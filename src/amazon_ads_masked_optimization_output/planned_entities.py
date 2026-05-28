"""Planned entity reservations and activation after readback."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional

from .registry import InMemoryRegistryProvider, RegistryEntry


@dataclass(frozen=True)
class PlannedEntity:
    handle: str
    entity_type: str
    status: str
    profile_id: Optional[str]


class PlannedEntityManager:
    """Coordinates planned handles for campaign creation workflows."""

    def __init__(self, registry: InMemoryRegistryProvider) -> None:
        self.registry = registry

    def reserve_campaign_plan(
        self,
        *,
        profile_id: str,
        plan_key: str,
        campaign_label: str,
        ad_group_label: str,
        keyword_labels: Iterable[str] = (),
        target_labels: Iterable[str] = (),
    ) -> Dict[str, List[PlannedEntity] | PlannedEntity]:
        campaign = self._planned("campaign", profile_id, f"{plan_key}:campaign", campaign_label)
        ad_group = self._planned("ad_group", profile_id, f"{plan_key}:ad_group", ad_group_label)
        keywords = [
            self._planned("keyword", profile_id, f"{plan_key}:keyword:{index}:{label}", label)
            for index, label in enumerate(keyword_labels, start=1)
        ]
        targets = [
            self._planned("target", profile_id, f"{plan_key}:target:{index}:{label}", label)
            for index, label in enumerate(target_labels, start=1)
        ]
        return {
            "campaign": campaign,
            "ad_group": ad_group,
            "keywords": keywords,
            "targets": targets,
        }

    def activate_from_readback(self, readback_rows: Iterable[Mapping[str, str]]) -> List[PlannedEntity]:
        activated: List[PlannedEntity] = []
        for row in readback_rows:
            entry = self.registry.activate_planned(
                row["handle"],
                raw_id=row["raw_id"],
                raw_label=row.get("raw_label"),
            )
            activated.append(self._to_planned_entity(entry))
        return activated

    def _planned(self, entity_type: str, profile_id: str, natural_key: str, label: str) -> PlannedEntity:
        return self._to_planned_entity(
            self.registry.reserve_planned(
                entity_type,
                natural_key=natural_key,
                label=label,
                profile_id=profile_id,
            )
        )

    @staticmethod
    def _to_planned_entity(entry: RegistryEntry) -> PlannedEntity:
        return PlannedEntity(
            handle=entry.handle,
            entity_type=entry.entity_type,
            status=entry.status,
            profile_id=entry.profile_id,
        )
