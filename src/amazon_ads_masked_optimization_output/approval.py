"""Approval packet and private execution manifest builders."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

from .errors import PrivatePathError, SanitizedError, StaleApprovalError
from .masking import MaskingResolver
from .registry import InMemoryRegistryProvider


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def isoformat(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ActionIdFactory:
    """Packet-local action id generator that does not derive ids from source data."""

    def __init__(self, *, prefix: str = "ACTION") -> None:
        self.prefix = prefix
        self._next = 1

    def new(self) -> str:
        action_id = f"{self.prefix}-{self._next:06d}"
        self._next += 1
        return action_id


@dataclass(frozen=True)
class ApprovalAction:
    action_type: str
    profile_id: str
    entity_type: str
    entity_id: str
    entity_label: Optional[str]
    current_values: Mapping[str, Any]
    proposed_values: Mapping[str, Any]
    exact_metrics: Mapping[str, Any]
    rationale: str
    raw_payload: Mapping[str, Any]


class ApprovalPacketBuilder:
    """Builds masked approval packets while preserving exact KPIs."""

    def __init__(
        self,
        resolver: MaskingResolver,
        *,
        packet_version: str = "2026-05-28",
        stale_after_hours: int = 24,
    ) -> None:
        self.resolver = resolver
        self.packet_version = packet_version
        self.stale_after_hours = stale_after_hours

    def build(
        self,
        actions: Sequence[ApprovalAction | Mapping[str, Any]],
        *,
        created_at: Optional[datetime] = None,
        action_id_factory: Optional[ActionIdFactory] = None,
    ) -> Dict[str, Any]:
        now = created_at or utc_now()
        factory = action_id_factory or ActionIdFactory()
        masked_actions: List[Dict[str, Any]] = []
        for action in actions:
            action_map = self._coerce_action(action)
            profile_handle = self.resolver.handle("profile", raw_id=str(action_map["profile_id"]))
            entity_handle = self.resolver.handle(
                str(action_map["entity_type"]),
                raw_id=str(action_map["entity_id"]),
                label=action_map.get("entity_label"),
                profile_id=str(action_map["profile_id"]),
            )
            masked_actions.append(
                {
                    "action_id": factory.new(),
                    "status": "APPROVAL_REQUIRED",
                    "profile": profile_handle,
                    "entity": {
                        "type": action_map["entity_type"],
                        "handle": entity_handle,
                    },
                    "action_type": action_map["action_type"],
                    "current_values": dict(action_map["current_values"]),
                    "proposed_values": dict(action_map["proposed_values"]),
                    "exact_metrics": dict(action_map["exact_metrics"]),
                    "rationale": self.resolver.mask_text(str(action_map["rationale"])),
                    "preflight_required": True,
                    "readback_required": True,
                    "execution": "not_in_skill_scope",
                }
            )
        packet = {
            "packet_version": self.packet_version,
            "created_at": isoformat(now),
            "expires_at": isoformat(now + timedelta(hours=self.stale_after_hours)),
            "actions": masked_actions,
            "public_output": True,
            "contains_raw_identifiers": False,
        }
        packet["packet_hash"] = packet_hash(packet)
        return packet

    def assert_fresh(self, packet: Mapping[str, Any], *, now: Optional[datetime] = None) -> None:
        expires_at = parse_utc(str(packet["expires_at"]))
        if (now or utc_now()) > expires_at:
            raise StaleApprovalError()

    def _coerce_action(self, action: ApprovalAction | Mapping[str, Any]) -> Mapping[str, Any]:
        if isinstance(action, ApprovalAction):
            return {
                "action_type": action.action_type,
                "profile_id": action.profile_id,
                "entity_type": action.entity_type,
                "entity_id": action.entity_id,
                "entity_label": action.entity_label,
                "current_values": action.current_values,
                "proposed_values": action.proposed_values,
                "exact_metrics": action.exact_metrics,
                "rationale": action.rationale,
                "raw_payload": action.raw_payload,
            }
        return action


class PrivateManifestBuilder:
    """Builds private execution manifests for a separate approved execution tool."""

    def __init__(self, registry: InMemoryRegistryProvider) -> None:
        self.registry = registry

    def build(
        self,
        actions: Sequence[ApprovalAction | Mapping[str, Any]],
        approval_packet: Mapping[str, Any],
    ) -> Dict[str, Any]:
        masked_actions = list(approval_packet["actions"])
        if len(masked_actions) != len(actions):
            raise SanitizedError("Approval packet and private manifest action counts differ.", code="MANIFEST_MISMATCH")
        private_actions: List[Dict[str, Any]] = []
        for raw_action, masked_action in zip(actions, masked_actions):
            action_map = raw_action if isinstance(raw_action, Mapping) else raw_action.__dict__
            private_actions.append(
                {
                    "action_id": masked_action["action_id"],
                    "profile_id": action_map["profile_id"],
                    "entity_type": action_map["entity_type"],
                    "entity_id": action_map["entity_id"],
                    "current_values": dict(action_map["current_values"]),
                    "proposed_values": dict(action_map["proposed_values"]),
                    "raw_payload": dict(action_map["raw_payload"]),
                    "requires_explicit_approval": True,
                    "requires_live_preflight": True,
                    "requires_readback": True,
                }
            )
        return {
            "private_manifest": True,
            "public_output": False,
            "approval_packet_hash": approval_packet["packet_hash"],
            "actions": private_actions,
        }

    def write(self, manifest: Mapping[str, Any], directory: str | Path, *, filename: str = "execution-manifest.private.json") -> Path:
        target_dir = Path(directory).expanduser().resolve()
        if not _is_private_directory(target_dir):
            raise PrivatePathError()
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / filename
        target.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        return target


def packet_hash(packet: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in packet.items() if key != "packet_hash"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "PACKET-" + hashlib.sha256(encoded).hexdigest()[:16].upper()


def parse_utc(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def _is_private_directory(path: Path) -> bool:
    private_root = os.environ.get("PRIVATE_TEST_DATA_DIR")
    parts = {part.casefold() for part in path.parts}
    if ".private" in parts or "private-test-data" in parts or path.name.casefold() == "private":
        return True
    if private_root:
        try:
            path.relative_to(Path(private_root).expanduser().resolve())
            return True
        except ValueError:
            return False
    return False


def sanitize_api_readback(readback: Iterable[Mapping[str, Any]], resolver: MaskingResolver) -> List[Dict[str, Any]]:
    """Convert raw API readback rows into masked status rows."""

    rows: List[Dict[str, Any]] = []
    for row in readback:
        profile_id = str(row["profile_id"])
        entity_type = str(row["entity_type"])
        rows.append(
            {
                "action_id": row["action_id"],
                "profile": resolver.handle("profile", raw_id=profile_id),
                "entity": {
                    "type": entity_type,
                    "handle": resolver.handle(
                        entity_type,
                        raw_id=str(row["entity_id"]),
                        label=row.get("entity_label"),
                        profile_id=profile_id,
                    ),
                },
                "readback_status": row.get("readback_status", "READBACK_CONFIRMED"),
                "current_values": dict(row.get("current_values", {})),
            }
        )
    return rows
