"""Synthetic end-to-end optimization flow with source-plane analysis."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping

from .approval import ApprovalAction, ApprovalPacketBuilder, PrivateManifestBuilder, sanitize_api_readback
from .masking import MaskingResolver
from .metrics import as_decimal, group_sum_by_source, rank_groups_by_metric
from .planned_entities import PlannedEntityManager
from .registry import InMemoryRegistryProvider
from .scanners import LeakScanner


METRIC_FIELDS = ("spend", "sales", "orders", "clicks", "impressions")


def diagnose_campaigns(records: Iterable[Mapping[str, Any]], resolver: MaskingResolver) -> List[Dict[str, Any]]:
    """Produce display-plane campaign diagnostics after source-plane grouping."""

    records_list = list(records)
    source_groups = rank_groups_by_metric(
        group_sum_by_source(records_list, group_field="campaign_id", metric_fields=METRIC_FIELDS),
        metric_field="spend",
        reverse=True,
    )
    diagnostics: List[Dict[str, Any]] = []
    for group in source_groups:
        campaign_id = str(group["campaign_id"])
        profile_id = _first_profile_for_campaign(records_list, campaign_id)
        campaign_name = _first_campaign_name(records_list, campaign_id)
        profile_handle = resolver.handle("profile", raw_id=profile_id)
        campaign_handle = resolver.handle("campaign", raw_id=campaign_id, label=campaign_name, profile_id=profile_id)
        diagnostics.append(
            {
                "profile": profile_handle,
                "campaign": campaign_handle,
                "source_rank": group["source_rank"],
                "spend": group["spend"],
                "sales": group["sales"],
                "orders": group["orders"],
                "clicks": group["clicks"],
                "impressions": group["impressions"],
            }
        )
    return diagnostics


def recommend_actions(records: Iterable[Mapping[str, Any]]) -> List[ApprovalAction]:
    """Recommend bid, budget, negative, and harvest actions from exact source records."""

    actions: List[ApprovalAction] = []
    for record in records:
        spend = as_decimal(record["spend"])
        sales = as_decimal(record["sales"])
        orders = as_decimal(record["orders"])
        target_acos = as_decimal(record.get("target_acos", "0.30"))
        acos = spend / sales if sales else None
        profile_id = str(record["profile_id"])
        campaign_id = str(record["campaign_id"])
        target_id = str(record["target_id"])

        if orders == 0 and spend >= Decimal("25"):
            actions.append(
                ApprovalAction(
                    action_type="bid_down",
                    profile_id=profile_id,
                    entity_type="target",
                    entity_id=target_id,
                    entity_label=str(record.get("keyword") or record.get("search_term") or "target"),
                    current_values={"bid": str(record["current_bid"])},
                    proposed_values={"bid": _money(as_decimal(record["current_bid"]) * Decimal("0.80"))},
                    exact_metrics=_metrics(record),
                    rationale=f"High spend with zero orders in {record['campaign_name']} for {record.get('search_term', 'target')}.",
                    raw_payload={"targetId": target_id, "bid": _money(as_decimal(record["current_bid"]) * Decimal("0.80"))},
                )
            )
            actions.append(
                ApprovalAction(
                    action_type="negative_exact",
                    profile_id=profile_id,
                    entity_type="search_term",
                    entity_id=str(record["search_term_id"]),
                    entity_label=str(record["search_term"]),
                    current_values={"negative": "absent"},
                    proposed_values={"negative": "exact"},
                    exact_metrics=_metrics(record),
                    rationale=f"Block waste term {record['search_term']} only after approval and live preflight.",
                    raw_payload={"campaignId": campaign_id, "matchType": "NEGATIVE_EXACT", "expression": record["search_term"]},
                )
            )

        if acos is not None and acos <= target_acos and as_decimal(record.get("budget_utilization", "0")) >= Decimal("0.95"):
            proposed_budget = as_decimal(record["current_budget"]) * Decimal("1.20")
            actions.append(
                ApprovalAction(
                    action_type="budget_increase",
                    profile_id=profile_id,
                    entity_type="campaign",
                    entity_id=campaign_id,
                    entity_label=str(record["campaign_name"]),
                    current_values={"daily_budget": str(record["current_budget"])},
                    proposed_values={"daily_budget": _money(proposed_budget)},
                    exact_metrics=_metrics(record),
                    rationale=f"Budget-capped efficient traffic in {record['campaign_name']} with exact KPIs preserved.",
                    raw_payload={"campaignId": campaign_id, "dailyBudget": _money(proposed_budget)},
                )
            )

        if orders >= Decimal("3") and acos is not None and acos <= target_acos:
            actions.append(
                ApprovalAction(
                    action_type="harvest_exact_keyword",
                    profile_id=profile_id,
                    entity_type="search_term",
                    entity_id=str(record["search_term_id"]),
                    entity_label=str(record["search_term"]),
                    current_values={"exact_keyword": "absent"},
                    proposed_values={"exact_keyword": "create"},
                    exact_metrics=_metrics(record),
                    rationale=f"Harvest converting search term {record['search_term']} from source campaign {record['campaign_name']}.",
                    raw_payload={"sourceCampaignId": campaign_id, "searchTerm": record["search_term"]},
                )
            )
    return actions


def build_masked_optimization_output(
    records: List[Mapping[str, Any]],
    registry: InMemoryRegistryProvider,
) -> Dict[str, Any]:
    resolver = MaskingResolver(registry)
    diagnostics = diagnose_campaigns(records, resolver)
    actions = recommend_actions(records)
    packet = ApprovalPacketBuilder(resolver).build(actions)
    manifest = PrivateManifestBuilder(registry).build(actions, packet)
    readback_rows = [
        {
            "action_id": action["action_id"],
            "profile_id": raw_action.profile_id,
            "entity_type": raw_action.entity_type,
            "entity_id": raw_action.entity_id,
            "entity_label": raw_action.entity_label,
            "current_values": raw_action.proposed_values,
            "readback_status": "READBACK_CONFIRMED",
        }
        for action, raw_action in zip(packet["actions"], actions)
    ]
    readback = sanitize_api_readback(readback_rows, resolver)
    public_output = {
        "diagnostics": diagnostics,
        "approval_packet": packet,
        "readback": readback,
        "coverage": registry.coverage_summary(),
    }
    LeakScanner(registry).assert_clean(LeakScanner(registry).scan_json(public_output, location="masked_output"))
    return {
        "public_output": public_output,
        "private_manifest": manifest,
    }


def plan_creation_entities(
    registry: InMemoryRegistryProvider,
    *,
    profile_id: str,
    plan_key: str,
) -> Dict[str, Any]:
    manager = PlannedEntityManager(registry)
    return manager.reserve_campaign_plan(
        profile_id=profile_id,
        plan_key=plan_key,
        campaign_label="Synthetic planned campaign",
        ad_group_label="Synthetic planned ad group",
        keyword_labels=["synthetic exact keyword"],
        target_labels=["synthetic product target"],
    )


def _first_profile_for_campaign(records: Iterable[Mapping[str, Any]], campaign_id: str) -> str:
    for record in records:
        if str(record["campaign_id"]) == campaign_id:
            return str(record["profile_id"])
    return "profile-unknown"


def _first_campaign_name(records: Iterable[Mapping[str, Any]], campaign_id: str) -> str | None:
    for record in records:
        if str(record["campaign_id"]) == campaign_id and record.get("campaign_name"):
            return str(record["campaign_name"])
    return None


def _metrics(record: Mapping[str, Any]) -> Dict[str, Any]:
    return {field: str(record[field]) for field in METRIC_FIELDS}


def _money(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), "f")
