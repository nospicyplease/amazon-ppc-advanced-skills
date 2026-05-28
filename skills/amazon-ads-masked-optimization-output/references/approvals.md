# Approvals Reference

This skill creates approval packets, not Amazon Ads mutations.

Approval packet rows must include:

- Immutable non-sensitive `action_id`.
- Masked profile and entity handles.
- Action type.
- Current values and proposed values.
- Exact metrics used by the recommendation.
- Rationale with masked identifiers only.
- Preflight required, explicit approval required, readback required, and monitoring required.
- Expiration or stale-approval policy.

Private execution manifests may contain raw IDs and payloads, but only for a separate approved execution tool. They must be written to ignored private paths and must never appear in public/demo output.

If live state differs from the approved current value, mark `STALE_APPROVAL` and require refreshed preflight and approval.
