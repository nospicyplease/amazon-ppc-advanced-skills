# Rubric

## Pass Criteria

- Detects destination negative conflict.
- Blocks approval readiness until conflict is resolved.
- Separates negative removal from keyword creation.
- Requires preflight, readback, and monitoring.

## Fail Criteria

- Harvests into a blocked destination.
- Treats negative conflict as a later cleanup item.
- Omits exact negative ID or approval gates.
- Marks row approval-ready.
