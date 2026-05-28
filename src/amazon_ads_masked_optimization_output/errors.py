"""Sanitized exception types for masked optimization workflows."""

from __future__ import annotations


class SanitizedError(Exception):
    """Base exception that never exposes raw identifiers in its message."""

    def __init__(self, safe_message: str, *, code: str = "SANITIZED_ERROR") -> None:
        super().__init__(safe_message)
        self.safe_message = safe_message
        self.code = code

    def __str__(self) -> str:
        return f"{self.code}: {self.safe_message}"


class MissingSecretError(SanitizedError):
    def __init__(self) -> None:
        super().__init__(
            "A tenant HMAC secret is required for text-only identifier masking.",
            code="MISSING_HMAC_SECRET",
        )


class RegistryCollisionError(SanitizedError):
    def __init__(self, safe_message: str = "Masking registry collision blocked.") -> None:
        super().__init__(safe_message, code="REGISTRY_COLLISION")


class UnsafeAliasError(SanitizedError):
    def __init__(self) -> None:
        super().__init__(
            "Unsafe source-derived alias blocked by masking registry.",
            code="UNSAFE_ALIAS",
        )


class StaleApprovalError(SanitizedError):
    def __init__(self) -> None:
        super().__init__(
            "Approval packet is stale and requires refreshed preflight.",
            code="STALE_APPROVAL",
        )


class LeakDetectedError(SanitizedError):
    def __init__(self, count: int) -> None:
        super().__init__(
            f"Leak scanner found {count} unsafe public artifact issue(s).",
            code="LEAK_DETECTED",
        )


class PrivatePathError(SanitizedError):
    def __init__(self) -> None:
        super().__init__(
            "Private execution manifests must be written only to ignored private paths.",
            code="PRIVATE_PATH_REQUIRED",
        )
