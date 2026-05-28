"""Display-plane masking helpers."""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, Mapping, Optional

from .errors import SanitizedError
from .registry import HANDLE_PREFIXES, InMemoryRegistryProvider, RegistryEntry


HANDLE_RE = re.compile(r"\b(?:ACCOUNT|PROFILE|PROJECT|PRODUCT|ASIN|SKU|CAMPAIGN|ADGROUP|KW|ST|TARGET|PLACEMENT|FILE|URL|ID)-\d{6}\b")
URL_RE = re.compile(r"https?://[^\s)\]}\"']+", re.IGNORECASE)


class MaskingResolver:
    """Resolves private source identifiers into stable public handles."""

    def __init__(self, registry: InMemoryRegistryProvider) -> None:
        self.registry = registry

    def handle(
        self,
        entity_type: str,
        *,
        raw_id: Optional[str] = None,
        label: Optional[str] = None,
        profile_id: Optional[str] = None,
        aliases: Optional[Iterable[str]] = None,
        allow_placeholder: bool = False,
        placeholder_key: Optional[str] = None,
    ) -> str:
        return self.entry(
            entity_type,
            raw_id=raw_id,
            label=label,
            profile_id=profile_id,
            aliases=aliases,
            allow_placeholder=allow_placeholder,
            placeholder_key=placeholder_key,
        ).handle

    def entry(
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
        return self.registry.lookup_or_create(
            entity_type,
            raw_id=raw_id,
            label=label,
            profile_id=profile_id,
            aliases=aliases,
            allow_placeholder=allow_placeholder,
            placeholder_key=placeholder_key,
        )

    def mask_record(
        self,
        record: Mapping[str, Any],
        entity_map: Mapping[str, str],
        *,
        profile_id_field: str = "profile_id",
    ) -> Dict[str, Any]:
        """Return a display-plane copy of a record with configured fields masked.

        ``entity_map`` maps record field name to registry entity type. Fields not in the map
        are copied exactly. Metric fields are never rounded or perturbed by this method.
        """

        profile_id = str(record.get(profile_id_field)) if record.get(profile_id_field) is not None else None
        masked: Dict[str, Any] = {}
        for field, value in record.items():
            entity_type = entity_map.get(field)
            if entity_type is None:
                masked[field] = value
                continue
            if value in (None, ""):
                masked[field] = self.handle(
                    entity_type,
                    profile_id=profile_id,
                    allow_placeholder=True,
                    placeholder_key=f"{field}:{profile_id or 'tenant'}",
                )
            else:
                raw_id = str(value) if field.endswith("_id") or entity_type in {"asin", "sku"} else None
                label = None if raw_id else str(value)
                masked[field] = self.handle(entity_type, raw_id=raw_id, label=label, profile_id=profile_id)
        return masked

    def mask_text(self, text: str, *, entity_type: str = "source_id", profile_id: Optional[str] = None) -> str:
        """Mask known private values and coarse URL patterns in user-facing text."""

        if not isinstance(text, str):
            raise SanitizedError("Only text values can be masked as text.", code="BAD_TEXT_VALUE")
        masked = text
        replacements: list[tuple[str, str]] = []
        for entry in self.registry.iter_entries():
            for value in entry.private_values():
                replacements.append((value, entry.handle))
        replacements.sort(key=lambda pair: len(pair[0]), reverse=True)
        for raw_value, handle in replacements:
            if not raw_value:
                continue
            masked = re.sub(re.escape(raw_value), handle, masked, flags=re.IGNORECASE)

        def replace_url(match: re.Match[str]) -> str:
            return self.handle("url", label=match.group(0), profile_id=profile_id)

        return URL_RE.sub(replace_url, masked)

    @staticmethod
    def is_handle(value: str) -> bool:
        return bool(HANDLE_RE.fullmatch(value))

    @staticmethod
    def expected_prefix(entity_type: str) -> str:
        return HANDLE_PREFIXES[entity_type]
