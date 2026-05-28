"""Create and check ignored local scaffolding for private real-profile dry-runs."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from .real_profile_dry_run import REQUIRED_REAL_ENV


README = """# Private real-profile dry-run data

This directory is ignored by git. Keep real Amazon Ads read-only fixtures, masking registries,
and local notes here. Do not move these files into public examples, docs, evals, or commits.

Required files for a real validation run:

- registry.json
- profile-<profile_id>.json for every id in AMAZON_ADS_PROFILE_IDS

Run:

make test-real-dry-run
make production-readiness
"""


REGISTRY_TEMPLATE: Dict[str, Any] = {
    "tenant_id": "replace-with-private-tenant-id",
    "entries": [],
    "unsafe_aliases": []
}


PROFILE_TEMPLATE: Dict[str, Any] = {
    "fixture_kind": "real_profile_read_only",
    "profile_id": "replace-with-profile-id",
    "records": [
        {
            "profile_id": "replace-with-profile-id",
            "campaign_id": "replace-with-campaign-id",
            "campaign_name": "replace-with-private-campaign-name",
            "target_id": "replace-with-target-id",
            "search_term_id": "replace-with-search-term-id",
            "search_term": "replace-with-private-search-term",
            "keyword": "replace-with-private-keyword",
            "asin": "replace-with-asin",
            "sku": "replace-with-sku",
            "spend": "0.00",
            "sales": "0.00",
            "orders": "0",
            "clicks": "0",
            "impressions": "0",
            "current_bid": "0.00",
            "current_budget": "0.00",
            "budget_utilization": "0",
            "target_acos": "0.30"
        }
    ]
}


PLACEHOLDER_MARKERS = ("replace-with", "dummy", "example", "placeholder", "todo")


def prepare_private_dry_run_dir() -> Path:
    target = Path(os.environ.get("PRIVATE_TEST_DATA_DIR", "private-test-data")).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    _write_if_missing(target / "README.local.md", README)
    _write_json_if_missing(target / "registry.template.json", REGISTRY_TEMPLATE)
    _write_json_if_missing(target / "profile.template.json", PROFILE_TEMPLATE)
    return target


def check_private_dry_run_config() -> Dict[str, Any]:
    env_status = _check_env()
    private_dir = Path(os.environ.get("PRIVATE_TEST_DATA_DIR", "private-test-data")).expanduser().resolve()
    files_status = _check_files(private_dir)
    ready = not env_status["issues"] and not files_status["issues"]
    return {
        "ready": ready,
        "private_dir_configured": bool(os.environ.get("PRIVATE_TEST_DATA_DIR")),
        "private_dir_exists": private_dir.exists(),
        "private_dir": str(private_dir),
        "env": env_status,
        "files": files_status,
        "live_execution": os.environ.get("ALLOW_LIVE_EXECUTION_TESTS", "false") == "true",
    }


def _check_env() -> Dict[str, Any]:
    missing = [name for name in REQUIRED_REAL_ENV if not os.environ.get(name)]
    placeholder = [
        name
        for name in REQUIRED_REAL_ENV
        if os.environ.get(name) and _looks_placeholder(os.environ[name])
    ]
    issues: List[str] = []
    if os.environ.get("ALLOW_REAL_PROFILE_TESTS") != "true":
        issues.append("ALLOW_REAL_PROFILE_TESTS is not true.")
    if missing:
        issues.append(f"Missing required env vars: {', '.join(missing)}.")
    if placeholder:
        issues.append(f"Placeholder-looking env vars: {', '.join(sorted(placeholder))}.")
    if os.environ.get("ALLOW_LIVE_EXECUTION_TESTS") == "true":
        issues.append("ALLOW_LIVE_EXECUTION_TESTS is true; keep it false unless a separate approved adapter and allowlist exist.")
    return {
        "required_present": not missing,
        "placeholder_free": not placeholder,
        "issues": issues,
    }


def _check_files(private_dir: Path) -> Dict[str, Any]:
    issues: List[str] = []
    registry_uri = os.environ.get("MASKING_REGISTRY_URI", "registry.json")
    profile_ids = [item.strip() for item in os.environ.get("AMAZON_ADS_PROFILE_IDS", "").split(",") if item.strip()]
    registry_path = _resolve_registry_path(registry_uri, private_dir)
    profile_paths = [private_dir / f"profile-{profile_id}.json" for profile_id in profile_ids]
    if not private_dir.exists():
        issues.append("PRIVATE_TEST_DATA_DIR does not exist.")
    if not registry_path.exists():
        issues.append("Masking registry fixture is missing.")
    else:
        issues.extend(_json_placeholder_issues(registry_path, label="registry"))
    if not profile_ids:
        issues.append("No profile ids configured.")
    for path in profile_paths:
        if not path.exists():
            issues.append("A profile fixture is missing.")
        else:
            issues.extend(_json_placeholder_issues(path, label="profile fixture"))
    return {
        "registry_exists": registry_path.exists(),
        "profiles_configured": len(profile_ids),
        "profile_fixtures_found": sum(1 for path in profile_paths if path.exists()),
        "issues": issues,
    }


def _resolve_registry_path(registry_uri: str, private_dir: Path) -> Path:
    if registry_uri.startswith("file://"):
        return Path(registry_uri[7:]).expanduser().resolve()
    raw = Path(registry_uri).expanduser()
    return (private_dir / raw).resolve() if not raw.is_absolute() else raw.resolve()


def _json_placeholder_issues(path: Path, *, label: str) -> List[str]:
    try:
        text = path.read_text(encoding="utf-8")
        json.loads(text)
    except (OSError, json.JSONDecodeError):
        return [f"{label} is not readable valid JSON."]
    if _looks_placeholder(text):
        return [f"{label} still contains placeholder-looking values."]
    return []


def _looks_placeholder(value: str) -> bool:
    normalized = value.casefold()
    return any(marker in normalized for marker in PLACEHOLDER_MARKERS)


def _write_if_missing(path: Path, text: str) -> None:
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def _write_json_if_missing(path: Path, value: Dict[str, Any]) -> None:
    if not path.exists():
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check ignored private dry-run config without printing secrets.")
    args = parser.parse_args()
    if args.check:
        result = check_private_dry_run_config()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ready"] else 1
    path = prepare_private_dry_run_dir()
    print(f"Prepared ignored private dry-run directory: {path}")
    print("Copy templates to registry.json and profile-<profile_id>.json, then fill them with private read-only data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
