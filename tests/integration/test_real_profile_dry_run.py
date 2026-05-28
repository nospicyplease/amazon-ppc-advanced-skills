from __future__ import annotations

import os
import json
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from amazon_ads_masked_optimization_output.real_profile_dry_run import (
    require_live_execution_adapter,
    run_real_profile_dry_run_from_env,
)
from amazon_ads_masked_optimization_output.errors import SanitizedError


class RealProfileDryRunTests(unittest.TestCase):
    def test_real_profile_dry_run_is_gated(self) -> None:
        old = os.environ.get("ALLOW_REAL_PROFILE_TESTS")
        os.environ.pop("ALLOW_REAL_PROFILE_TESTS", None)
        try:
            result = run_real_profile_dry_run_from_env()
        finally:
            if old is not None:
                os.environ["ALLOW_REAL_PROFILE_TESTS"] = old
        self.assertEqual(result.status, "SKIPPED")
        self.assertEqual(result.profiles_checked, 0)

    def test_live_execution_tests_require_explicit_adapter(self) -> None:
        old = os.environ.get("ALLOW_LIVE_EXECUTION_TESTS")
        os.environ.pop("ALLOW_LIVE_EXECUTION_TESTS", None)
        try:
            with self.assertRaises(SanitizedError):
                require_live_execution_adapter()
        finally:
            if old is not None:
                os.environ["ALLOW_LIVE_EXECUTION_TESTS"] = old

    def test_placeholder_sensitive_env_blocks_real_profile_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            private_dir = Path(tmp) / "private-test-data"
            private_dir.mkdir()
            with patched_env(
                {
                    "ALLOW_REAL_PROFILE_TESTS": "true",
                    "AMAZON_ADS_CLIENT_ID": "dummy",
                    "AMAZON_ADS_CLIENT_SECRET": "replace-with-client-secret",
                    "AMAZON_ADS_REFRESH_TOKEN": "dummy",
                    "AMAZON_ADS_PROFILE_IDS": "1234567890123456",
                    "MASKING_REGISTRY_URI": "registry.json",
                    "MASKING_HMAC_SECRET": "synthetic-secret",
                    "PRIVATE_TEST_DATA_DIR": str(private_dir),
                }
            ):
                result = run_real_profile_dry_run_from_env()
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("Placeholder-looking", result.message)

    def test_placeholder_profile_id_blocks_real_profile_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            private_dir = Path(tmp) / "private-test-data"
            private_dir.mkdir()
            with patched_env(
                {
                    "ALLOW_REAL_PROFILE_TESTS": "true",
                    "AMAZON_ADS_CLIENT_ID": "amzn1.application-oa2-client.local",
                    "AMAZON_ADS_CLIENT_SECRET": "local-secret-value-that-is-not-template",
                    "AMAZON_ADS_REFRESH_TOKEN": "Atzr|local-read-only-token",
                    "AMAZON_ADS_PROFILE_IDS": "replace-with-profile-id",
                    "MASKING_REGISTRY_URI": "registry.json",
                    "MASKING_HMAC_SECRET": "0123456789abcdef0123456789abcdef",
                    "PRIVATE_TEST_DATA_DIR": str(private_dir),
                }
            ):
                result = run_real_profile_dry_run_from_env()
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("AMAZON_ADS_PROFILE_IDS", result.message)

    def test_placeholder_registry_file_blocks_before_private_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            private_dir = Path(tmp) / "private-test-data"
            private_dir.mkdir()
            (private_dir / "registry.json").write_text(
                json.dumps({"tenant_id": "replace-with-private-tenant-id", "entries": []}),
                encoding="utf-8",
            )
            with patched_env(
                {
                    "ALLOW_REAL_PROFILE_TESTS": "true",
                    "AMAZON_ADS_CLIENT_ID": "amzn1.application-oa2-client.local",
                    "AMAZON_ADS_CLIENT_SECRET": "local-secret-value-that-is-not-template",
                    "AMAZON_ADS_REFRESH_TOKEN": "Atzr|local-read-only-token",
                    "AMAZON_ADS_PROFILE_IDS": "1234567890123456",
                    "MASKING_REGISTRY_URI": "registry.json",
                    "MASKING_HMAC_SECRET": "0123456789abcdef0123456789abcdef",
                    "PRIVATE_TEST_DATA_DIR": str(private_dir),
                }
            ):
                result = run_real_profile_dry_run_from_env()
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("registry fixture", result.message)
        self.assertNotIn("replace-with-private-tenant-id", result.message)

    def test_placeholder_profile_fixture_blocks_before_private_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            private_dir = Path(tmp) / "private-test-data"
            private_dir.mkdir()
            (private_dir / "registry.json").write_text(
                json.dumps({"tenant_id": "tenant_private_test", "entries": []}),
                encoding="utf-8",
            )
            (private_dir / "profile-1234567890123456.json").write_text(
                json.dumps(
                    {
                        "fixture_kind": "real_profile_read_only",
                        "profile_id": "1234567890123456",
                        "records": [_record("1234567890123456") | {"campaign_name": "replace-with-campaign"}],
                    }
                ),
                encoding="utf-8",
            )
            with patched_env(
                {
                    "ALLOW_REAL_PROFILE_TESTS": "true",
                    "AMAZON_ADS_CLIENT_ID": "amzn1.application-oa2-client.local",
                    "AMAZON_ADS_CLIENT_SECRET": "local-secret-value-that-is-not-template",
                    "AMAZON_ADS_REFRESH_TOKEN": "Atzr|local-read-only-token",
                    "AMAZON_ADS_PROFILE_IDS": "1234567890123456",
                    "MASKING_REGISTRY_URI": "registry.json",
                    "MASKING_HMAC_SECRET": "0123456789abcdef0123456789abcdef",
                    "PRIVATE_TEST_DATA_DIR": str(private_dir),
                }
            ):
                result = run_real_profile_dry_run_from_env()
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("fixture", result.message)
        self.assertNotIn("replace-with-campaign", result.message)

    def test_private_multi_profile_fixture_can_pass_without_printing_raw_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            private_dir = Path(tmp) / "private-test-data"
            private_dir.mkdir()
            (private_dir / "registry.json").write_text(
                json.dumps({"tenant_id": "tenant_private_test", "entries": []}),
                encoding="utf-8",
            )
            profiles = ["1234567890123456", "2345678901234567"]
            for profile in profiles:
                (private_dir / f"profile-{profile}.json").write_text(
                    json.dumps(
                        {
                            "fixture_kind": "real_profile_read_only",
                            "profile_id": profile,
                            "records": [_record(profile)],
                        }
                    ),
                    encoding="utf-8",
                )
            with patched_env(
                {
                    "ALLOW_REAL_PROFILE_TESTS": "true",
                    "AMAZON_ADS_CLIENT_ID": "amzn1.application-oa2-client.syntheticlocalonly",
                    "AMAZON_ADS_CLIENT_SECRET": "local-secret-value-that-is-not-a-placeholder",
                    "AMAZON_ADS_REFRESH_TOKEN": "Atzr|local-read-only-fixture-token",
                    "AMAZON_ADS_PROFILE_IDS": ",".join(profiles),
                    "MASKING_REGISTRY_URI": "registry.json",
                    "MASKING_HMAC_SECRET": "0123456789abcdef0123456789abcdef",
                    "PRIVATE_TEST_DATA_DIR": str(private_dir),
                    "ALLOW_LIVE_EXECUTION_TESTS": "false",
                }
            ):
                result = run_real_profile_dry_run_from_env()
        self.assertEqual(result.status, "PASSED")
        self.assertEqual(result.profiles_checked, 2)
        self.assertEqual(result.registry_status, "PRIVATE_FILE_REGISTRY")
        self.assertNotIn(profiles[0], str(result.safe_dict()))


def _record(profile_id: str) -> dict[str, str]:
    return {
        "profile_id": profile_id,
        "campaign_id": f"campaign-{profile_id}",
        "campaign_name": f"Private Fixture Campaign {profile_id}",
        "target_id": f"target-{profile_id}",
        "search_term_id": f"term-{profile_id}",
        "search_term": f"private fixture query {profile_id}",
        "keyword": f"private fixture keyword {profile_id}",
        "asin": "B0PRIVT001",
        "sku": f"SKU-PRIVATE-{profile_id}",
        "spend": "10.00",
        "sales": "100.00",
        "orders": "4",
        "clicks": "20",
        "impressions": "2000",
        "current_bid": "1.00",
        "current_budget": "25.00",
        "budget_utilization": "0.97",
        "target_acos": "0.20",
    }


@contextmanager
def patched_env(values: dict[str, str]) -> Iterator[None]:
    old = {name: os.environ.get(name) for name in values}
    try:
        for name, value in values.items():
            os.environ[name] = value
        yield
    finally:
        for name, value in old.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


if __name__ == "__main__":
    unittest.main()
