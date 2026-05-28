from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from amazon_ads_masked_optimization_output.private_setup import check_private_dry_run_config, prepare_private_dry_run_dir


class PrivateSetupTests(unittest.TestCase):
    def test_prepare_private_dry_run_dir_writes_templates_without_overwrite(self) -> None:
        old = os.environ.get("PRIVATE_TEST_DATA_DIR")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "private-test-data"
            os.environ["PRIVATE_TEST_DATA_DIR"] = str(target)
            prepared = prepare_private_dry_run_dir()
            self.assertEqual(prepared, target.resolve())
            registry_template = prepared / "registry.template.json"
            profile_template = prepared / "profile.template.json"
            self.assertTrue((prepared / "README.local.md").exists())
            self.assertEqual(json.loads(registry_template.read_text(encoding="utf-8"))["entries"], [])
            profile_template.write_text("private operator notes stay intact", encoding="utf-8")
            prepare_private_dry_run_dir()
            self.assertEqual(profile_template.read_text(encoding="utf-8"), "private operator notes stay intact")
        if old is None:
            os.environ.pop("PRIVATE_TEST_DATA_DIR", None)
        else:
            os.environ["PRIVATE_TEST_DATA_DIR"] = old

    def test_check_private_dry_run_config_reports_placeholders_safely(self) -> None:
        old = {name: os.environ.get(name) for name in [
            "ALLOW_REAL_PROFILE_TESTS",
            "AMAZON_ADS_CLIENT_ID",
            "AMAZON_ADS_CLIENT_SECRET",
            "AMAZON_ADS_REFRESH_TOKEN",
            "AMAZON_ADS_PROFILE_IDS",
            "MASKING_REGISTRY_URI",
            "MASKING_HMAC_SECRET",
            "PRIVATE_TEST_DATA_DIR",
            "ALLOW_LIVE_EXECUTION_TESTS",
        ]}
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "private-test-data"
            os.environ.update(
                {
                    "ALLOW_REAL_PROFILE_TESTS": "true",
                    "AMAZON_ADS_CLIENT_ID": "replace-with-client-id",
                    "AMAZON_ADS_CLIENT_SECRET": "replace-with-secret",
                    "AMAZON_ADS_REFRESH_TOKEN": "replace-with-token",
                    "AMAZON_ADS_PROFILE_IDS": "replace-with-profile-id",
                    "MASKING_REGISTRY_URI": "registry.json",
                    "MASKING_HMAC_SECRET": "replace-with-private-hmac-secret-minimum-32-chars",
                    "PRIVATE_TEST_DATA_DIR": str(target),
                    "ALLOW_LIVE_EXECUTION_TESTS": "false",
                }
            )
            prepare_private_dry_run_dir()
            (target / "registry.json").write_text('{"tenant_id":"replace-with-tenant","entries":[]}', encoding="utf-8")
            (target / "profile-replace-with-profile-id.json").write_text(
                '{"fixture_kind":"real_profile_read_only","profile_id":"replace-with-profile-id","records":[]}',
                encoding="utf-8",
            )
            result = check_private_dry_run_config()
        self.assertFalse(result["ready"])
        self.assertIn("Placeholder-looking env vars", " ".join(result["env"]["issues"]))
        self.assertNotIn("replace-with-client-id", str(result))
        for name, value in old.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


if __name__ == "__main__":
    unittest.main()
