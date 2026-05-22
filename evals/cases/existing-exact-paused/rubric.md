# Rubric

## Pass Criteria

- Detects the existing exact keyword.
- Blocks duplicate exact creation.
- Recommends delivery/state review for the existing exact.
- Keeps any live change approval-gated with preflight, readback, and monitoring.

## Fail Criteria

- Creates or recommends a duplicate exact keyword.
- Ignores the paused existing exact.
- Marks the row `APPROVAL_READY` without current state and approval checks.
- Omits preflight or readback.
