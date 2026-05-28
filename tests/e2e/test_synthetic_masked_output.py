from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from amazon_ads_masked_optimization_output.errors import RegistryCollisionError
from amazon_ads_masked_optimization_output.optimization import (
    build_masked_optimization_output,
    plan_creation_entities,
)
from amazon_ads_masked_optimization_output.registry import SyntheticFileRegistryProvider
from amazon_ads_masked_optimization_output.scanners import LeakScanner
from amazon_ads_masked_optimization_output.synthetic_loader import load_synthetic_fixture


FIXTURE = Path("examples/amazon-ads-masked-optimization-output/sample-data/synthetic-profile.json")


class SyntheticE2ETests(unittest.TestCase):
    def setUp(self) -> None:
        loaded = load_synthetic_fixture(FIXTURE, hmac_secret="synthetic-secret")
        self.records = loaded["records"]
        self.registry = loaded["registry"]

    def test_diagnostics_bid_budget_negatives_harvesting_approvals_and_readback(self) -> None:
        result = build_masked_optimization_output(self.records, self.registry)
        public = result["public_output"]
        actions = public["approval_packet"]["actions"]
        action_types = {action["action_type"] for action in actions}

        self.assertEqual(public["diagnostics"][0]["campaign"], "CAMPAIGN-000002")
        self.assertEqual(public["diagnostics"][0]["spend"], "30.00")
        self.assertIn("bid_down", action_types)
        self.assertIn("budget_increase", action_types)
        self.assertIn("negative_exact", action_types)
        self.assertIn("harvest_exact_keyword", action_types)
        self.assertTrue(all(action["status"] == "APPROVAL_REQUIRED" for action in actions))
        self.assertTrue(all(row["readback_status"] == "READBACK_CONFIRMED" for row in public["readback"]))
        self.assertNotIn("camp_syn", json.dumps(public))
        self.assertNotIn("Synthetic Alpha Launch", json.dumps(public))

    def test_creation_plan_reserves_and_activates_planned_entities(self) -> None:
        plan = plan_creation_entities(self.registry, profile_id="profile_syn_us_001", plan_key="creation-plan-001")
        self.assertEqual(plan["campaign"].status, "planned")
        activated = self.registry.activate_planned(
            plan["campaign"].handle,
            raw_id="created_campaign_syn_001",
            raw_label="Created Synthetic Campaign",
        )
        self.assertEqual(activated.status, "active")

    def test_multi_profile_output_pairs_profile_and_campaign_handles(self) -> None:
        result = build_masked_optimization_output(self.records, self.registry)
        diagnostics = result["public_output"]["diagnostics"]
        profile_campaign_pairs = {(row["profile"], row["campaign"]) for row in diagnostics}
        self.assertIn(("PROFILE-000001", "CAMPAIGN-000001"), profile_campaign_pairs)
        self.assertIn(("PROFILE-000002", "CAMPAIGN-000001"), profile_campaign_pairs)

    def test_collision_blocking(self) -> None:
        registry = SyntheticFileRegistryProvider.from_file(FIXTURE, hmac_secret="synthetic-secret")
        with self.assertRaises(RegistryCollisionError):
            registry.import_entry(
                entity_type="campaign",
                handle="CAMPAIGN-000001",
                raw_id="different-campaign",
                profile_id="profile_syn_us_001",
            )

    def test_public_artifact_scan_passes_and_private_manifest_is_separate(self) -> None:
        result = build_masked_optimization_output(self.records, self.registry)
        with tempfile.TemporaryDirectory() as tmp:
            public_path = Path(tmp) / "public-output.json"
            public_path.write_text(json.dumps(result["public_output"], indent=2), encoding="utf-8")
            scanner = LeakScanner(self.registry, flag_generic_urls=True)
            scanner.assert_clean(scanner.scan_path(public_path))
        self.assertIn("profile_syn", json.dumps(result["private_manifest"]))
        self.assertNotIn("private_manifest", json.dumps(result["public_output"]))


if __name__ == "__main__":
    unittest.main()
