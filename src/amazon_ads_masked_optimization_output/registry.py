"""Tenant-scoped masking registry providers."""

from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, MutableMapping, Optional, Tuple

from .errors import MissingSecretError, RegistryCollisionError, SanitizedError, UnsafeAliasError


HANDLE_PREFIXES: Mapping[str, str] = {
    "account": "ACCOUNT",
    "profile": "PROFILE",
    "project": "PROJECT",
    "product": "PRODUCT",
    "asin": "ASIN",
    "sku": "SKU",
    "campaign": "CAMPAIGN",
    "ad_group": "ADGROUP",
    "keyword": "KW",
    "search_term": "ST",
    "target": "TARGET",
    "placement": "PLACEMENT",
    "filename": "FILE",
    "url": "URL",
    "source_id": "ID",
}

SAFE_STATUSES = {"active", "placeholder", "planned", "retired", "blocked"}
TEXT_ONLY_TYPES = {
    "keyword",
    "search_term",
    "target",
    "placement",
    "product",
    "project",
    "filename",
    "url",
    "source_id",
}


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def _assert_known_entity_type(entity_type: str) -> None:
    if entity_type not in HANDLE_PREFIXES:
        raise SanitizedError(f"Unknown masked entity type: {entity_type}", code="UNKNOWN_ENTITY_TYPE")


@dataclass
class RegistryEntry:
    tenant_id: str
    profile_id: Optional[str]
    entity_type: str
    source_key: str
    handle: str
    status: str = "active"
    raw_id: Optional[str] = None
    raw_label: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    planned: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def safe_dict(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "profile_scope": "tenant" if self.profile_id is None else "profile",
            "entity_type": self.entity_type,
            "handle": self.handle,
            "status": self.status,
            "planned": self.planned,
        }

    def private_values(self) -> List[str]:
        values = [self.raw_id, self.raw_label, *self.aliases]
        return [value for value in values if value]


class RegistryProvider:
    """Interface for tenant-scoped masking registries."""

    tenant_id: str

    def lookup_or_create(
        self,
        entity_type: str,
        *,
        raw_id: Optional[str] = None,
        label: Optional[str] = None,
        profile_id: Optional[str] = None,
        aliases: Optional[Iterable[str]] = None,
        allow_placeholder: bool = False,
        placeholder_key: Optional[str] = None,
    ) -> RegistryEntry:
        raise NotImplementedError

    def reserve_planned(
        self,
        entity_type: str,
        *,
        natural_key: str,
        label: Optional[str] = None,
        profile_id: Optional[str] = None,
    ) -> RegistryEntry:
        raise NotImplementedError

    def activate_planned(
        self,
        handle: str,
        *,
        raw_id: str,
        raw_label: Optional[str] = None,
    ) -> RegistryEntry:
        raise NotImplementedError

    def transition(self, handle: str, status: str) -> RegistryEntry:
        raise NotImplementedError

    def coverage_summary(self) -> Dict[str, Any]:
        raise NotImplementedError

    def iter_entries(self) -> Iterator[RegistryEntry]:
        raise NotImplementedError


class InMemoryRegistryProvider(RegistryProvider):
    """In-memory registry suitable for tests, demos, and adapters."""

    def __init__(self, tenant_id: str, *, hmac_secret: Optional[str] = None) -> None:
        self.tenant_id = tenant_id
        self.hmac_secret = hmac_secret
        self._entries_by_key: MutableMapping[Tuple[str, Optional[str], str, str], RegistryEntry] = {}
        self._entries_by_handle: MutableMapping[Tuple[Optional[str], str, str], RegistryEntry] = {}
        self._alias_index: MutableMapping[str, RegistryEntry] = {}
        self._unsafe_aliases: set[str] = set()
        self._counters: MutableMapping[Tuple[str, Optional[str]], int] = {}

    def lookup_or_create(
        self,
        entity_type: str,
        *,
        raw_id: Optional[str] = None,
        label: Optional[str] = None,
        profile_id: Optional[str] = None,
        aliases: Optional[Iterable[str]] = None,
        allow_placeholder: bool = False,
        placeholder_key: Optional[str] = None,
    ) -> RegistryEntry:
        _assert_known_entity_type(entity_type)
        private_aliases = list(aliases or [])
        source_key = self._source_key(
            entity_type,
            raw_id=raw_id,
            label=label,
            allow_placeholder=allow_placeholder,
            placeholder_key=placeholder_key,
        )
        key = (self.tenant_id, profile_id, entity_type, source_key)
        existing = self._entries_by_key.get(key)
        if existing:
            self._merge_private_values(existing, raw_id=raw_id, label=label, aliases=private_aliases)
            return existing
        self._assert_safe_aliases([value for value in [raw_id, label, *private_aliases] if value])

        status = "placeholder" if source_key.startswith("placeholder:") else "active"
        entry = RegistryEntry(
            tenant_id=self.tenant_id,
            profile_id=profile_id,
            entity_type=entity_type,
            source_key=source_key,
            handle=self._next_handle(entity_type, profile_id),
            status=status,
            raw_id=raw_id,
            raw_label=label,
            aliases=private_aliases,
            planned=False,
        )
        self._store(entry)
        return entry

    def import_entry(
        self,
        *,
        entity_type: str,
        handle: str,
        raw_id: Optional[str] = None,
        label: Optional[str] = None,
        profile_id: Optional[str] = None,
        aliases: Optional[Iterable[str]] = None,
        status: str = "active",
        planned: bool = False,
    ) -> RegistryEntry:
        _assert_known_entity_type(entity_type)
        if status not in SAFE_STATUSES:
            raise SanitizedError("Registry entry has an unsupported status.", code="BAD_STATUS")
        source_key = self._source_key(
            entity_type,
            raw_id=raw_id,
            label=label,
            allow_placeholder=status == "placeholder",
            placeholder_key=handle,
        )
        entry = RegistryEntry(
            tenant_id=self.tenant_id,
            profile_id=profile_id,
            entity_type=entity_type,
            source_key=source_key,
            handle=handle,
            status=status,
            raw_id=raw_id,
            raw_label=label,
            aliases=list(aliases or []),
            planned=planned,
        )
        self._store(entry)
        self._bump_counter_from_handle(entity_type, profile_id, handle)
        return entry

    def reserve_planned(
        self,
        entity_type: str,
        *,
        natural_key: str,
        label: Optional[str] = None,
        profile_id: Optional[str] = None,
    ) -> RegistryEntry:
        _assert_known_entity_type(entity_type)
        if not self.hmac_secret:
            raise MissingSecretError()
        source_key = "planned:" + self._hmac_digest(f"{entity_type}|{natural_key}")
        key = (self.tenant_id, profile_id, entity_type, source_key)
        existing = self._entries_by_key.get(key)
        if existing:
            return existing
        entry = RegistryEntry(
            tenant_id=self.tenant_id,
            profile_id=profile_id,
            entity_type=entity_type,
            source_key=source_key,
            handle=self._next_handle(entity_type, profile_id),
            status="planned",
            raw_label=label,
            planned=True,
        )
        self._store(entry)
        return entry

    def activate_planned(
        self,
        handle: str,
        *,
        raw_id: str,
        raw_label: Optional[str] = None,
    ) -> RegistryEntry:
        entry = self._lookup_handle(handle)
        if not entry or entry.status != "planned":
            raise SanitizedError("Planned masked entity was not found.", code="PLANNED_NOT_FOUND")
        new_source_key = self._source_key(entry.entity_type, raw_id=raw_id, label=raw_label)
        old_key = (entry.tenant_id, entry.profile_id, entry.entity_type, entry.source_key)
        new_key = (entry.tenant_id, entry.profile_id, entry.entity_type, new_source_key)
        existing = self._entries_by_key.get(new_key)
        if existing and existing.handle != handle:
            raise RegistryCollisionError()
        self._entries_by_key.pop(old_key, None)
        entry.source_key = new_source_key
        entry.raw_id = raw_id
        entry.raw_label = raw_label
        entry.status = "active"
        entry.planned = False
        self._entries_by_key[new_key] = entry
        self._index_aliases(entry)
        return entry

    def transition(self, handle: str, status: str) -> RegistryEntry:
        if status not in SAFE_STATUSES:
            raise SanitizedError("Unsupported registry status transition.", code="BAD_STATUS")
        entry = self._lookup_handle(handle)
        if not entry:
            raise SanitizedError("Masked registry handle was not found.", code="HANDLE_NOT_FOUND")
        entry.status = status
        return entry

    def register_unsafe_alias(self, alias: str) -> None:
        if alias:
            self._unsafe_aliases.add(normalize_text(alias))

    def coverage_summary(self) -> Dict[str, Any]:
        counts: Dict[str, Dict[str, int]] = {}
        for entry in self._entries_by_handle.values():
            bucket = counts.setdefault(entry.entity_type, {})
            bucket[entry.status] = bucket.get(entry.status, 0) + 1
        return {
            "tenant_id": self.tenant_id,
            "total_handles": len(self._entries_by_handle),
            "counts": counts,
            "unsafe_alias_count": len(self._unsafe_aliases),
            "contains_private_values": False,
        }

    def iter_entries(self) -> Iterator[RegistryEntry]:
        yield from self._entries_by_handle.values()

    def safe_snapshot(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "entries": [entry.safe_dict() for entry in self.iter_entries()],
            "coverage": self.coverage_summary(),
        }

    def private_values(self) -> List[str]:
        values: List[str] = []
        for entry in self.iter_entries():
            values.extend(entry.private_values())
        return values

    def _store(self, entry: RegistryEntry) -> None:
        key = (entry.tenant_id, entry.profile_id, entry.entity_type, entry.source_key)
        handle_key = (entry.profile_id, entry.entity_type, entry.handle)
        existing_for_key = self._entries_by_key.get(key)
        existing_for_handle = self._entries_by_handle.get(handle_key)
        if existing_for_key and existing_for_key.handle != entry.handle:
            raise RegistryCollisionError()
        if existing_for_handle and existing_for_handle.source_key != entry.source_key:
            raise RegistryCollisionError()
        self._entries_by_key[key] = entry
        self._entries_by_handle[handle_key] = entry
        self._index_aliases(entry)

    def _merge_private_values(
        self,
        entry: RegistryEntry,
        *,
        raw_id: Optional[str],
        label: Optional[str],
        aliases: Iterable[str],
    ) -> None:
        changed = False
        if raw_id and not entry.raw_id:
            entry.raw_id = raw_id
            changed = True
        if label and not entry.raw_label:
            entry.raw_label = label
            changed = True
        for alias in aliases:
            if alias and alias not in entry.aliases:
                entry.aliases.append(alias)
                changed = True
        if changed:
            self._index_aliases(entry)

    def _lookup_handle(self, handle: str) -> Optional[RegistryEntry]:
        matches = [entry for key, entry in self._entries_by_handle.items() if key[2] == handle]
        if not matches:
            return None
        if len(matches) > 1:
            raise SanitizedError("Masked handle is ambiguous without profile scope.", code="AMBIGUOUS_HANDLE")
        return matches[0]

    def _index_aliases(self, entry: RegistryEntry) -> None:
        for value in entry.private_values():
            normalized = normalize_text(value)
            existing = self._alias_index.get(normalized)
            if existing and existing.handle != entry.handle:
                raise RegistryCollisionError("A raw identifier resolves to multiple masked handles.")
            self._alias_index[normalized] = entry

    def _source_key(
        self,
        entity_type: str,
        *,
        raw_id: Optional[str] = None,
        label: Optional[str] = None,
        allow_placeholder: bool = False,
        placeholder_key: Optional[str] = None,
    ) -> str:
        if raw_id:
            return "id:" + normalize_text(raw_id)
        if label:
            if entity_type in TEXT_ONLY_TYPES:
                if not self.hmac_secret:
                    raise MissingSecretError()
                return "hmac:" + self._hmac_digest(f"{entity_type}|{normalize_text(label)}")
            return "label:" + normalize_text(label)
        if allow_placeholder:
            safe_key = placeholder_key or f"{entity_type}:{len(self._entries_by_handle) + 1}"
            return "placeholder:" + self._hmac_digest(safe_key) if self.hmac_secret else f"placeholder:{safe_key}"
        raise SanitizedError("Registry lookup requires a raw id, label, or placeholder permission.", code="LOOKUP_KEY_REQUIRED")

    def _assert_safe_aliases(self, values: Iterable[str]) -> None:
        for value in values:
            if normalize_text(value) in self._unsafe_aliases:
                raise UnsafeAliasError()

    def _hmac_digest(self, value: str) -> str:
        if not self.hmac_secret:
            raise MissingSecretError()
        return hmac.new(
            self.hmac_secret.encode("utf-8"),
            f"{self.tenant_id}|{value}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _next_handle(self, entity_type: str, profile_id: Optional[str]) -> str:
        key = (entity_type, profile_id)
        self._counters[key] = self._counters.get(key, 0) + 1
        return f"{HANDLE_PREFIXES[entity_type]}-{self._counters[key]:06d}"

    def _bump_counter_from_handle(self, entity_type: str, profile_id: Optional[str], handle: str) -> None:
        prefix = f"{HANDLE_PREFIXES[entity_type]}-"
        if not handle.startswith(prefix):
            return
        suffix = handle[len(prefix) :]
        if suffix.isdigit():
            key = (entity_type, profile_id)
            self._counters[key] = max(self._counters.get(key, 0), int(suffix))


class SyntheticFileRegistryProvider(InMemoryRegistryProvider):
    """Registry provider loaded from a synthetic JSON fixture."""

    @classmethod
    def from_file(
        cls,
        path: str | Path,
        *,
        tenant_id: Optional[str] = None,
        hmac_secret: Optional[str] = None,
    ) -> "SyntheticFileRegistryProvider":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        provider = cls(tenant_id or data["tenant_id"], hmac_secret=hmac_secret)
        for raw_alias in data.get("unsafe_aliases", []):
            provider.register_unsafe_alias(raw_alias)
        for item in data.get("entries", []):
            provider.import_entry(
                entity_type=item["entity_type"],
                handle=item["handle"],
                raw_id=item.get("raw_id"),
                label=item.get("raw_label"),
                profile_id=item.get("profile_id"),
                aliases=item.get("aliases", []),
                status=item.get("status", "active"),
                planned=item.get("planned", False),
            )
        return provider


class ExternalRegistryProviderStub(RegistryProvider):
    """Adapter placeholder for a tenant registry service."""

    def __init__(self, tenant_id: str, *, uri: str) -> None:
        self.tenant_id = tenant_id
        self.uri = uri

    def lookup_or_create(self, *args: Any, **kwargs: Any) -> RegistryEntry:
        raise SanitizedError("External masking registry adapter is not configured.", code="EXTERNAL_REGISTRY_STUB")

    def reserve_planned(self, *args: Any, **kwargs: Any) -> RegistryEntry:
        raise SanitizedError("External masking registry adapter is not configured.", code="EXTERNAL_REGISTRY_STUB")

    def activate_planned(self, *args: Any, **kwargs: Any) -> RegistryEntry:
        raise SanitizedError("External masking registry adapter is not configured.", code="EXTERNAL_REGISTRY_STUB")

    def transition(self, *args: Any, **kwargs: Any) -> RegistryEntry:
        raise SanitizedError("External masking registry adapter is not configured.", code="EXTERNAL_REGISTRY_STUB")

    def coverage_summary(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "external_registry": True,
            "uri_configured": bool(self.uri),
            "contains_private_values": False,
        }

    def iter_entries(self) -> Iterator[RegistryEntry]:
        return iter(())
