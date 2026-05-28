"""Synthetic fixture loading for masked optimization examples."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .registry import SyntheticFileRegistryProvider


def load_synthetic_fixture(path: str | Path, *, hmac_secret: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    registry = SyntheticFileRegistryProvider.from_file(
        path,
        tenant_id=data["tenant_id"],
        hmac_secret=hmac_secret,
    )
    return {
        "tenant_id": data["tenant_id"],
        "profiles": data.get("profiles", []),
        "records": data.get("records", []),
        "actions": data.get("actions", []),
        "readback": data.get("readback", []),
        "registry": registry,
    }
