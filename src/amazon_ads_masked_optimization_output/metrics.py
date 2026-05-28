"""Exact KPI validation and source-plane grouping."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from .errors import SanitizedError


def as_decimal(value: Any) -> Decimal:
    return Decimal(str(value))


class MetricValidator:
    """Validates that display output preserves analytical metrics exactly."""

    def __init__(self, metric_fields: Sequence[str]) -> None:
        self.metric_fields = tuple(metric_fields)

    def assert_record_metrics_preserved(
        self,
        source_records: Sequence[Mapping[str, Any]],
        display_records: Sequence[Mapping[str, Any]],
        *,
        source_id_field: str,
        display_id_field: str,
        id_map: Mapping[str, str],
    ) -> None:
        if len(source_records) != len(display_records):
            raise SanitizedError("Metric validation failed: record count changed.", code="METRIC_COUNT_CHANGED")
        display_by_handle = {str(record[display_id_field]): record for record in display_records}
        for source in source_records:
            handle = id_map[str(source[source_id_field])]
            display = display_by_handle.get(handle)
            if display is None:
                raise SanitizedError("Metric validation failed: masked record missing.", code="METRIC_RECORD_MISSING")
            for field in self.metric_fields:
                if as_decimal(source[field]) != as_decimal(display[field]):
                    raise SanitizedError("Metric validation failed: KPI value changed.", code="METRIC_CHANGED")

    def assert_group_metrics_preserved(
        self,
        source_groups: Sequence[Mapping[str, Any]],
        display_groups: Sequence[Mapping[str, Any]],
        *,
        source_id_field: str,
        display_id_field: str,
        id_map: Mapping[str, str],
    ) -> None:
        display_by_handle = {str(record[display_id_field]): record for record in display_groups}
        for source in source_groups:
            handle = id_map[str(source[source_id_field])]
            display = display_by_handle.get(handle)
            if not display:
                raise SanitizedError("Metric validation failed: masked group missing.", code="METRIC_GROUP_MISSING")
            for field in self.metric_fields:
                if as_decimal(source[field]) != as_decimal(display[field]):
                    raise SanitizedError("Metric validation failed: grouped KPI value changed.", code="METRIC_CHANGED")


def group_sum_by_source(
    records: Iterable[Mapping[str, Any]],
    *,
    group_field: str,
    metric_fields: Sequence[str],
) -> List[Dict[str, Any]]:
    """Group records by raw source field before masking and sum exact Decimal metrics."""

    grouped: Dict[str, Dict[str, Any]] = {}
    for record in records:
        group_id = str(record[group_field])
        bucket = grouped.setdefault(group_id, {group_field: group_id})
        for field in metric_fields:
            bucket[field] = bucket.get(field, Decimal("0")) + as_decimal(record.get(field, "0"))
    return [
        {
            key: (format(value, "f") if isinstance(value, Decimal) else value)
            for key, value in bucket.items()
        }
        for bucket in grouped.values()
    ]


def rank_groups_by_metric(
    groups: Iterable[Mapping[str, Any]],
    *,
    metric_field: str,
    reverse: bool = True,
) -> List[Dict[str, Any]]:
    """Rank source-plane groups by exact metric value."""

    ranked = sorted(
        (dict(group) for group in groups),
        key=lambda group: as_decimal(group[metric_field]),
        reverse=reverse,
    )
    for index, group in enumerate(ranked, start=1):
        group["source_rank"] = index
    return ranked


def exact_ratio(numerator: Any, denominator: Any) -> str | None:
    denominator_decimal = as_decimal(denominator)
    if denominator_decimal == 0:
        return None
    return format(as_decimal(numerator) / denominator_decimal, "f")
