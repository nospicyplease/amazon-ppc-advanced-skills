from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from amazon_ads_masked_optimization_output.readiness import build_readiness_report


class ReadinessTests(unittest.TestCase):
    def test_readiness_includes_sanitized_private_config_status(self) -> None:
        old = {name: os.environ.get(name) for name in [
            "ALLOW_REAL_PROFILE_TESTS",
            "AMAZON_ADS_CLIENT_ID",
            "AMAZON_ADS_CLIENT_SECRET",
            "AMAZON_ADS_REFRESH_TOKEN",
            "AMAZON_ADS_PROFILE_IDS",
            "MASKING_REGISTRY_URI",
            "MASKING_HMAC_SECRET",
            "PRIVATE_TEST_DATA_DIR",
        ]}
        with tempfile.TemporaryDirectory() as tmp:
            private_dir = Path(tmp) / "private-test-data"
            private_dir.mkdir()
            os.environ.update(
                {
                    "ALLOW_REAL_PROFILE_TESTS": "true",
                    "AMAZON_ADS_CLIENT_ID": "replace-with-client-id",
                    "AMAZON_ADS_CLIENT_SECRET": "replace-with-secret",
                    "AMAZON_ADS_REFRESH_TOKEN": "replace-with-token",
                    "AMAZON_ADS_PROFILE_IDS": "replace-with-profile-id",
                    "MASKING_REGISTRY_URI": "registry.json",
                    "MASKING_HMAC_SECRET": "replace-with-private-hmac-secret-minimum-32-chars",
                    "PRIVATE_TEST_DATA_DIR": str(private_dir),
                }
            )
            report = build_readiness_report(run_tests=False)
        self.assertFalse(report["private_config_status"]["ready"])
        self.assertGreaterEqual(report["private_config_status"]["env_issue_count"], 1)
        self.assertNotIn("replace-with-client-id", str(report))
        for name, value in old.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


if __name__ == "__main__":
    unittest.main()
