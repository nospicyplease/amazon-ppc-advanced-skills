"""Leak scanners for public artifacts, logs, and readbacks."""

from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Mapping, Optional, Sequence

from .errors import LeakDetectedError
from .registry import InMemoryRegistryProvider


PROMPT_INJECTION_RE = re.compile(
    r"(ignore\s+previous\s+instructions|reveal\s+the\s+system\s+prompt|developer\s+message|do\s+not\s+mask)",
    re.IGNORECASE,
)
CSV_FORMULA_RE = re.compile(r"(^|[\n,;])\s*[=+@][^\n,;]+")
URL_RE = re.compile(r"https?://[^\s)\]}\"']+", re.IGNORECASE)
ASIN_RE = re.compile(r"\bB0[A-Z0-9]{8}\b")
HMAC_RE = re.compile(r"\b[a-f0-9]{64}\b", re.IGNORECASE)


@dataclass(frozen=True)
class LeakFinding:
    kind: str
    location: str
    excerpt: str


class LeakScanner:
    """Scans text and files for unsafe public output."""

    def __init__(
        self,
        registry: Optional[InMemoryRegistryProvider] = None,
        *,
        extra_private_terms: Optional[Iterable[str]] = None,
        flag_generic_urls: bool = False,
        flag_generic_asins: bool = True,
    ) -> None:
        self.registry = registry
        private_values: List[str] = []
        if registry:
            private_values.extend(registry.private_values())
        private_values.extend(extra_private_terms or [])
        self.private_values = sorted(
            {value for value in private_values if value and len(value.strip()) >= 3},
            key=len,
            reverse=True,
        )
        self.flag_generic_urls = flag_generic_urls
        self.flag_generic_asins = flag_generic_asins

    def scan_text(self, text: str, *, location: str = "<text>") -> List[LeakFinding]:
        findings: List[LeakFinding] = []
        for value in self.private_values:
            if re.search(re.escape(value), text, flags=re.IGNORECASE):
                findings.append(LeakFinding("private_value", location, self._excerpt(text, value)))
        if self.flag_generic_urls:
            findings.extend(self._regex_findings(URL_RE, text, "url", location))
        if self.flag_generic_asins:
            findings.extend(self._regex_findings(ASIN_RE, text, "asin", location))
        findings.extend(self._regex_findings(PROMPT_INJECTION_RE, text, "prompt_injection", location))
        findings.extend(self._regex_findings(CSV_FORMULA_RE, text, "csv_formula", location))
        findings.extend(self._regex_findings(HMAC_RE, text, "hmac_digest", location))
        return findings

    def scan_json(self, value: Mapping[str, object] | Sequence[object], *, location: str = "<json>") -> List[LeakFinding]:
        return self.scan_text(json.dumps(value, sort_keys=True), location=location)

    def scan_path(self, path: str | Path) -> List[LeakFinding]:
        root = Path(path)
        findings: List[LeakFinding] = []
        if root.is_file():
            return self._scan_file(root)
        for file_path in root.rglob("*"):
            if file_path.is_file():
                findings.extend(self._scan_file(file_path))
        return findings

    def assert_clean(self, findings: Iterable[LeakFinding]) -> None:
        findings_list = list(findings)
        if findings_list:
            raise LeakDetectedError(len(findings_list))

    def _scan_file(self, path: Path) -> List[LeakFinding]:
        if path.suffix.lower() == ".xlsx":
            return self._scan_xlsx(path)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return []
        return self.scan_text(text, location=str(path))

    def _scan_xlsx(self, path: Path) -> List[LeakFinding]:
        findings: List[LeakFinding] = []
        try:
            with zipfile.ZipFile(path) as workbook:
                for name in workbook.namelist():
                    if name.endswith(".xml") or name.startswith("docProps/"):
                        text = workbook.read(name).decode("utf-8", errors="ignore")
                        findings.extend(self.scan_text(text, location=f"{path}:{name}"))
        except zipfile.BadZipFile:
            findings.append(LeakFinding("bad_xlsx", str(path), "unreadable xlsx artifact"))
        return findings

    @staticmethod
    def _regex_findings(pattern: re.Pattern[str], text: str, kind: str, location: str) -> List[LeakFinding]:
        return [LeakFinding(kind, location, match.group(0)[:120]) for match in pattern.finditer(text)]

    @staticmethod
    def _excerpt(text: str, needle: str) -> str:
        match = re.search(re.escape(needle), text, flags=re.IGNORECASE)
        if not match:
            return needle[:120]
        start = max(0, match.start() - 20)
        end = min(len(text), match.end() + 20)
        return text[start:end].replace("\n", "\\n")[:160]


def sanitize_for_log(message: str, scanner: LeakScanner, *, replacement: str = "[MASKED]") -> str:
    sanitized = message
    for value in scanner.private_values:
        sanitized = re.sub(re.escape(value), replacement, sanitized, flags=re.IGNORECASE)
    sanitized = URL_RE.sub(replacement, sanitized)
    sanitized = ASIN_RE.sub(replacement, sanitized)
    sanitized = PROMPT_INJECTION_RE.sub(replacement, sanitized)
    return sanitized
