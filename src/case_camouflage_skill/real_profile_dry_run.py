"""Read-only real-profile dry-run harness gated by environment variables."""

from __future__ import annotations

import json
import os
from json import JSONDecodeError
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from .approval import _is_private_directory
from .errors import SanitizedError
from .optimization import build_masked_optimization_output
from .registry import InMemoryRegistryProvider, SyntheticFileRegistryProvider
from .scanners import LeakScanner


REQUIRED_REAL_ENV = (
    "AMAZON_ADS_CLIENT_ID",
    "AMAZON_ADS_CLIENT_SECRET",
    "AMAZON_ADS_REFRESH_TOKEN",
    "AMAZON_ADS_PROFILE_IDS",
    "MASKING_REGISTRY_URI",
    "MASKING_HMAC_SECRET",
    "PRIVATE_TEST_DATA_DIR",
)

INSECURE_PLACEHOLDER_VALUES = {
    "changeme",
    "dummy",
    "example",
    "placeholder",
    "replace-with",
    "secret",
    "synthetic-secret",
    "test",
    "todo",
}

SENSITIVE_ENV = {
    "AMAZON_ADS_CLIENT_ID",
    "AMAZON_ADS_CLIENT_SECRET",
    "AMAZON_ADS_REFRESH_TOKEN",
    "MASKING_HMAC_SECRET",
}
PLACEHOLDER_ENV = SENSITIVE_ENV | {"AMAZON_ADS_PROFILE_IDS"}
PLACEHOLDER_FILE_MARKERS = ("replace-with", "placeholder", "todo", "dummy")


@dataclass(frozen=True)
class RealProfileDryRunResult:
    status: str
    profiles_checked: int
    message: str
    live_execution_status: str
    registry_status: str = "NOT_CONFIGURED"

    def safe_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "profiles_checked": self.profiles_checked,
            "message": self.message,
            "live_execution_status": self.live_execution_status,
            "registry_status": self.registry_status,
        }


def run_real_profile_dry_run_from_env() -> RealProfileDryRunResult:
    if os.environ.get("ALLOW_REAL_PROFILE_TESTS") != "true":
        return RealProfileDryRunResult(
            status="SKIPPED",
            profiles_checked=0,
            message="Set ALLOW_REAL_PROFILE_TESTS=true and configure private credentials to run read-only validation.",
            live_execution_status=_live_execution_status(),
            registry_status="NOT_CONFIGURED",
        )
    missing = [name for name in REQUIRED_REAL_ENV if not os.environ.get(name)]
    if missing:
        return RealProfileDryRunResult(
            status="BLOCKED",
            profiles_checked=0,
            message=f"Missing required real-profile env vars: {', '.join(missing)}.",
            live_execution_status=_live_execution_status(),
            registry_status="NOT_CONFIGURED",
        )
    insecure = _placeholder_env_vars()
    if insecure:
        return RealProfileDryRunResult(
            status="BLOCKED",
            profiles_checked=0,
            message=f"Placeholder-looking env vars are not accepted for real-profile validation: {', '.join(insecure)}.",
            live_execution_status=_live_execution_status(),
            registry_status="NOT_CONFIGURED",
        )

    private_dir = Path(os.environ["PRIVATE_TEST_DATA_DIR"]).expanduser().resolve()
    if not private_dir.exists():
        return RealProfileDryRunResult(
            status="BLOCKED",
            profiles_checked=0,
            message="Private test data directory does not exist.",
            live_execution_status=_live_execution_status(),
            registry_status="NOT_CONFIGURED",
        )
    if not _is_private_directory(private_dir):
        return RealProfileDryRunResult(
            status="BLOCKED",
            profiles_checked=0,
            message="PRIVATE_TEST_DATA_DIR must be an ignored private path.",
            live_execution_status=_live_execution_status(),
            registry_status="NOT_CONFIGURED",
        )

    profile_ids = [item.strip() for item in os.environ["AMAZON_ADS_PROFILE_IDS"].split(",") if item.strip()]
    if not profile_ids:
        return RealProfileDryRunResult(
            status="BLOCKED",
            profiles_checked=0,
            message="At least one Amazon Ads profile id must be configured.",
            live_execution_status=_live_execution_status(),
            registry_status="NOT_CONFIGURED",
        )
    hmac_secret = os.environ["MASKING_HMAC_SECRET"]
    registry, registry_status = _load_private_registry(
        os.environ["MASKING_REGISTRY_URI"],
        private_dir=private_dir,
        hmac_secret=hmac_secret,
    )
    if registry is None:
        return RealProfileDryRunResult(
            status="BLOCKED",
            profiles_checked=0,
            message=registry_status,
            live_execution_status=_live_execution_status(),
            registry_status="BLOCKED",
        )
    profiles_checked = 0
    for profile_id in profile_ids:
        fixture = private_dir / f"profile-{profile_id}.json"
        if not fixture.exists():
            return RealProfileDryRunResult(
                status="BLOCKED",
                profiles_checked=profiles_checked,
                message="Private dry-run fixture missing for at least one configured profile.",
                live_execution_status=_live_execution_status(),
                registry_status=registry_status,
            )
        try:
            fixture_text = fixture.read_text(encoding="utf-8")
            if _contains_file_placeholder(fixture_text):
                return RealProfileDryRunResult(
                    status="BLOCKED",
                    profiles_checked=profiles_checked,
                    message="Private dry-run fixture still contains placeholder-looking values.",
                    live_execution_status=_live_execution_status(),
                    registry_status=registry_status,
                )
            data = json.loads(fixture_text)
            _validate_private_fixture(data, expected_profile_id=profile_id)
            output = build_masked_optimization_output(data.get("records", []), registry)["public_output"]
            scanner = LeakScanner(registry, extra_private_terms=[profile_id], flag_generic_urls=True)
            scanner.assert_clean(scanner.scan_json(output, location=f"profile-{profiles_checked + 1}"))
        except (JSONDecodeError, OSError, SanitizedError):
            return RealProfileDryRunResult(
                status="FAILED",
                profiles_checked=profiles_checked,
                message="Private dry-run failed with sanitized validation or scanning errors.",
                live_execution_status=_live_execution_status(),
                registry_status=registry_status,
            )
        profiles_checked += 1

    return RealProfileDryRunResult(
        status="PASSED",
        profiles_checked=profiles_checked,
        message="Read-only real-profile dry-run passed with masked public output.",
        live_execution_status=_live_execution_status(),
        registry_status=registry_status,
    )


def require_live_execution_adapter() -> None:
    if os.environ.get("ALLOW_LIVE_EXECUTION_TESTS") != "true":
        raise SanitizedError("Live execution tests are disabled by default.", code="LIVE_EXECUTION_DISABLED")
    if not os.environ.get("LIVE_EXECUTION_ALLOWLIST"):
        raise SanitizedError("Live execution allowlist is required.", code="LIVE_ALLOWLIST_REQUIRED")
    if not os.environ.get("LIVE_EXECUTION_ADAPTER"):
        raise SanitizedError("Separate live execution adapter is required.", code="LIVE_ADAPTER_REQUIRED")


def _live_execution_status() -> str:
    if os.environ.get("ALLOW_LIVE_EXECUTION_TESTS") == "true":
        if os.environ.get("LIVE_EXECUTION_ALLOWLIST") and os.environ.get("LIVE_EXECUTION_ADAPTER"):
            return "CONFIGURED_BUT_NOT_RUN_BY_SKILL"
        return "BLOCKED_MISSING_ALLOWLIST_OR_ADAPTER"
    return "DISABLED"


def _placeholder_env_vars() -> List[str]:
    insecure: List[str] = []
    for name in sorted(PLACEHOLDER_ENV):
        value = os.environ.get(name, "").strip()
        normalized = value.casefold()
        if (
            normalized in INSECURE_PLACEHOLDER_VALUES
            or normalized.startswith("dummy")
            or normalized.startswith("example")
            or normalized.startswith("replace")
            or normalized.startswith("todo")
        ):
            insecure.append(name)
    if len(os.environ.get("MASKING_HMAC_SECRET", "")) < 32:
        insecure.append("MASKING_HMAC_SECRET")
    return sorted(set(insecure))


def _load_private_registry(
    uri: str,
    *,
    private_dir: Path,
    hmac_secret: str,
) -> tuple[InMemoryRegistryProvider | None, str]:
    if uri.startswith("file://"):
        registry_path = Path(uri[7:]).expanduser().resolve()
    elif "://" in uri:
        return None, "External masking registry adapters are not enabled for local dry-run validation."
    else:
        raw_path = Path(uri).expanduser()
        registry_path = (private_dir / raw_path).resolve() if not raw_path.is_absolute() else raw_path.resolve()
    try:
        registry_path.relative_to(private_dir)
    except ValueError:
        if not _is_private_directory(registry_path.parent):
            return None, "MASKING_REGISTRY_URI must point to an ignored private registry fixture."
    if not registry_path.exists():
        return None, "Private masking registry fixture does not exist."
    try:
        if _contains_file_placeholder(registry_path.read_text(encoding="utf-8")):
            return None, "Private masking registry fixture still contains placeholder-looking values."
        return SyntheticFileRegistryProvider.from_file(registry_path, hmac_secret=hmac_secret), "PRIVATE_FILE_REGISTRY"
    except (JSONDecodeError, OSError, SanitizedError):
        return None, "Private masking registry fixture could not be loaded safely."


def _validate_private_fixture(data: Dict[str, Any], *, expected_profile_id: str) -> None:
    if data.get("fixture_kind") != "real_profile_read_only":
        raise SanitizedError("Private dry-run fixture kind is not accepted.", code="BAD_PRIVATE_FIXTURE")
    if data.get("profile_id") != expected_profile_id:
        raise SanitizedError("Private dry-run fixture profile mismatch.", code="PRIVATE_PROFILE_MISMATCH")
    records = data.get("records")
    if not isinstance(records, list) or not records:
        raise SanitizedError("Private dry-run fixture has no records.", code="PRIVATE_RECORDS_REQUIRED")
    for record in records:
        if not isinstance(record, dict) or record.get("profile_id") != expected_profile_id:
            raise SanitizedError("Private dry-run record profile mismatch.", code="PRIVATE_RECORD_PROFILE_MISMATCH")


def _contains_file_placeholder(value: str) -> bool:
    normalized = value.casefold()
    return any(marker in normalized for marker in PLACEHOLDER_FILE_MARKERS)


def main() -> int:
    result = run_real_profile_dry_run_from_env()
    print(json.dumps(result.safe_dict(), indent=2, sort_keys=True))
    return 0 if result.status in {"PASSED", "SKIPPED", "BLOCKED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
