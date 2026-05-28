from __future__ import annotations

import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from amazon_ads_masked_optimization_output.approval import (
    ApprovalAction,
    ApprovalPacketBuilder,
    PrivateManifestBuilder,
    utc_now,
)
from amazon_ads_masked_optimization_output.errors import (
    MissingSecretError,
    RegistryCollisionError,
    SanitizedError,
    StaleApprovalError,
    UnsafeAliasError,
)
from amazon_ads_masked_optimization_output.masking import MaskingResolver
from amazon_ads_masked_optimization_output.metrics import MetricValidator, group_sum_by_source, rank_groups_by_metric
from amazon_ads_masked_optimization_output.planned_entities import PlannedEntityManager
from amazon_ads_masked_optimization_output.registry import InMemoryRegistryProvider


class RegistryTests(unittest.TestCase):
    def test_lookup_is_stable_and_profile_scoped(self) -> None:
        registry = InMemoryRegistryProvider("tenant", hmac_secret="secret")
        first = registry.lookup_or_create("campaign", raw_id="camp-1", label="Campaign One", profile_id="profile-a")
        again = registry.lookup_or_create("campaign", raw_id="camp-1", label="Campaign One", profile_id="profile-a")
        other_profile = registry.lookup_or_create("campaign", raw_id="camp-1", label="Campaign One", profile_id="profile-b")
        self.assertEqual(first.handle, again.handle)
        self.assertEqual(first.handle, "CAMPAIGN-000001")
        self.assertEqual(other_profile.handle, "CAMPAIGN-000001")
        self.assertNotEqual(first.profile_id, other_profile.profile_id)

    def test_collision_blocks_duplicate_handle_for_different_source(self) -> None:
        registry = InMemoryRegistryProvider("tenant", hmac_secret="secret")
        registry.import_entry(entity_type="campaign", handle="CAMPAIGN-000001", raw_id="camp-a", profile_id="profile")
        with self.assertRaises(RegistryCollisionError):
            registry.import_entry(entity_type="campaign", handle="CAMPAIGN-000001", raw_id="camp-b", profile_id="profile")

    def test_unsafe_alias_blocks_lookup_without_exposing_alias(self) -> None:
        registry = InMemoryRegistryProvider("tenant", hmac_secret="secret")
        registry.register_unsafe_alias("Raw Customer Campaign")
        with self.assertRaises(UnsafeAliasError) as ctx:
            registry.lookup_or_create("campaign", raw_id="camp-a", label="Raw Customer Campaign")
        self.assertNotIn("Raw Customer Campaign", str(ctx.exception))

    def test_placeholder_and_status_transition(self) -> None:
        registry = InMemoryRegistryProvider("tenant", hmac_secret="secret")
        entry = registry.lookup_or_create("asin", allow_placeholder=True, placeholder_key="missing-asin")
        self.assertEqual(entry.status, "placeholder")
        registry.transition(entry.handle, "blocked")
        self.assertEqual(registry.coverage_summary()["counts"]["asin"]["blocked"], 1)

    def test_text_identifier_requires_hmac_secret_and_hides_digest(self) -> None:
        with self.assertRaises(MissingSecretError):
            InMemoryRegistryProvider("tenant").lookup_or_create("search_term", label="raw query")
        registry = InMemoryRegistryProvider("tenant", hmac_secret="secret")
        entry = registry.lookup_or_create("search_term", label="raw query")
        safe = entry.safe_dict()
        self.assertEqual(entry.handle, "ST-000001")
        self.assertNotIn("source_key", safe)
        self.assertNotIn("raw query", str(safe))


class MetricTests(unittest.TestCase):
    def test_grouping_and_ranking_use_source_ids_before_masking(self) -> None:
        records = [
            {"campaign_id": "camp-b", "spend": "10.10", "sales": "100.00"},
            {"campaign_id": "camp-a", "spend": "30.05", "sales": "0.00"},
            {"campaign_id": "camp-b", "spend": "0.90", "sales": "9.99"},
        ]
        grouped = group_sum_by_source(records, group_field="campaign_id", metric_fields=("spend", "sales"))
        ranked = rank_groups_by_metric(grouped, metric_field="spend")
        self.assertEqual(ranked[0]["campaign_id"], "camp-a")
        self.assertEqual(ranked[1]["campaign_id"], "camp-b")
        self.assertEqual(ranked[1]["spend"], "11.00")

    def test_metric_preservation_detects_changes(self) -> None:
        validator = MetricValidator(["spend", "sales"])
        source = [{"target_id": "target-1", "spend": "12.340", "sales": "100.00"}]
        display = [{"target": "TARGET-000001", "spend": "12.34", "sales": "100.00"}]
        validator.assert_record_metrics_preserved(
            source,
            display,
            source_id_field="target_id",
            display_id_field="target",
            id_map={"target-1": "TARGET-000001"},
        )
        changed = [{"target": "TARGET-000001", "spend": "12.35", "sales": "100.00"}]
        with self.assertRaises(SanitizedError):
            validator.assert_record_metrics_preserved(
                source,
                changed,
                source_id_field="target_id",
                display_id_field="target",
                id_map={"target-1": "TARGET-000001"},
            )


class ApprovalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = InMemoryRegistryProvider("tenant", hmac_secret="secret")
        self.resolver = MaskingResolver(self.registry)
        self.action = ApprovalAction(
            action_type="bid_down",
            profile_id="profile-raw-1",
            entity_type="target",
            entity_id="target-raw-1",
            entity_label="raw keyword",
            current_values={"bid": "1.50"},
            proposed_values={"bid": "1.20"},
            exact_metrics={"spend": "30.00", "sales": "0.00", "orders": "0"},
            rationale="Raw Campaign spent on raw keyword.",
            raw_payload={"targetId": "target-raw-1", "bid": "1.20"},
        )

    def test_approval_packet_masks_public_values_and_action_ids(self) -> None:
        self.registry.lookup_or_create("campaign", raw_id="camp-raw-1", label="Raw Campaign")
        packet = ApprovalPacketBuilder(self.resolver).build([self.action])
        action = packet["actions"][0]
        self.assertEqual(action["action_id"], "ACTION-000001")
        self.assertEqual(action["profile"], "PROFILE-000001")
        self.assertEqual(action["entity"]["handle"], "TARGET-000001")
        self.assertEqual(action["exact_metrics"]["spend"], "30.00")
        self.assertNotIn("target-raw-1", str(packet))
        self.assertNotIn("Raw Campaign", str(packet))

    def test_private_manifest_contains_raw_payload_but_requires_private_path(self) -> None:
        packet = ApprovalPacketBuilder(self.resolver).build([self.action])
        manifest = PrivateManifestBuilder(self.registry).build([self.action], packet)
        self.assertEqual(manifest["actions"][0]["entity_id"], "target-raw-1")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SanitizedError):
                PrivateManifestBuilder(self.registry).write(manifest, Path(tmp) / "public")
            path = PrivateManifestBuilder(self.registry).write(manifest, Path(tmp) / ".private")
            self.assertTrue(path.exists())

    def test_stale_packet_is_blocked(self) -> None:
        created = utc_now() - timedelta(hours=25)
        builder = ApprovalPacketBuilder(self.resolver, stale_after_hours=24)
        packet = builder.build([self.action], created_at=created)
        with self.assertRaises(StaleApprovalError):
            builder.assert_fresh(packet, now=utc_now())

    def test_planned_reservation_and_activation_after_readback(self) -> None:
        manager = PlannedEntityManager(self.registry)
        plan = manager.reserve_campaign_plan(
            profile_id="profile-raw-1",
            plan_key="plan-001",
            campaign_label="Planned Raw Campaign",
            ad_group_label="Planned Raw Ad Group",
            keyword_labels=["planned keyword"],
            target_labels=["planned target"],
        )
        campaign = plan["campaign"]
        self.assertEqual(campaign.status, "planned")
        activated = manager.activate_from_readback(
            [{"handle": campaign.handle, "raw_id": "campaign-created-1", "raw_label": "Created Raw Campaign"}]
        )
        self.assertEqual(activated[0].status, "active")

    def test_sanitized_error_does_not_echo_raw_context(self) -> None:
        error = SanitizedError("Lookup failed for masked entity.", code="LOOKUP_FAILED")
        self.assertNotIn("raw keyword", str(error))


if __name__ == "__main__":
    unittest.main()
