"""Production readiness report for the masked optimization package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from .private_setup import check_private_dry_run_config
from .real_profile_dry_run import run_real_profile_dry_run_from_env


TEST_COMMANDS = {
    "unit": [sys.executable, "-m", "unittest", "discover", "-s", "tests/unit", "-p", "test_*.py"],
    "e2e": [sys.executable, "-m", "unittest", "discover", "-s", "tests/e2e", "-p", "test_*.py"],
    "leakage": [sys.executable, "-m", "unittest", "discover", "-s", "tests/leakage", "-p", "test_*.py"],
}


def build_readiness_report(*, run_tests: bool = True, cwd: Optional[Path] = None) -> Dict[str, Any]:
    root = cwd or Path.cwd()
    test_results = _run_tests(root) if run_tests else {}
    private_config = _private_config_summary()
    real_profile = run_real_profile_dry_run_from_env().safe_dict()
    synthetic_ok = all(result.get("passed") for name, result in test_results.items() if name in {"unit", "e2e", "leakage"})
    real_ok = real_profile["status"] == "PASSED"
    limitations: List[str] = []
    if not synthetic_ok:
        limitations.append("Synthetic unit, E2E, and leakage tests must pass.")
    if not real_ok:
        limitations.append("Read-only real-profile dry-runs have not passed in this environment.")
    if not private_config["ready"]:
        limitations.append("Private dry-run configuration is incomplete or still contains placeholders.")
    live_status = real_profile["live_execution_status"]
    live_guard_ok = live_status in {"DISABLED", "CONFIGURED_BUT_NOT_RUN_BY_SKILL"}
    if live_status == "DISABLED":
        limitations.append("Live execution is intentionally disabled; this skill remains read-only.")
    elif not live_guard_ok:
        limitations.append("Live execution was requested but lacks a separate approved adapter and allowlist.")
    verdict = "PRODUCTION_READY" if synthetic_ok and real_ok and live_guard_ok else "NOT_PRODUCTION_READY"
    return {
        "package": "case-camouflage-skill",
        "tests": test_results,
        "scanner_coverage": {
            "public_artifacts": "text, json, xlsx XML, hidden sheets, metadata, stdout, stderr",
            "blocked_patterns": "registry private values, ASINs, URLs when enabled, prompt injection, CSV formulas, HMAC digests",
        },
        "private_config_status": private_config,
        "real_profile_status": real_profile,
        "live_execution_status": real_profile["live_execution_status"],
        "limitations": limitations,
        "verdict": verdict,
    }


def _private_config_summary() -> Dict[str, Any]:
    try:
        status = check_private_dry_run_config()
    except Exception:
        return {
            "ready": False,
            "env_issue_count": 1,
            "file_issue_count": 1,
            "profiles_configured": 0,
            "profile_fixtures_found": 0,
        }
    return {
        "ready": bool(status.get("ready")),
        "env_issue_count": len(status.get("env", {}).get("issues", [])),
        "file_issue_count": len(status.get("files", {}).get("issues", [])),
        "profiles_configured": status.get("files", {}).get("profiles_configured", 0),
        "profile_fixtures_found": status.get("files", {}).get("profile_fixtures_found", 0),
        "live_execution": bool(status.get("live_execution")),
    }


def _run_tests(root: Path) -> Dict[str, Dict[str, Any]]:
    results: Dict[str, Dict[str, Any]] = {}
    for name, command in TEST_COMMANDS.items():
        completed = subprocess.run(
            command,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        results[name] = {
            "passed": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-1200:],
            "stderr_tail": completed.stderr[-1200:],
        }
    return results


def main() -> int:
    report = build_readiness_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
