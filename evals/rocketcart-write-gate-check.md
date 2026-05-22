# Rocketcart Write Gate Check

Use this review prompt before any Rocketcart MCP write is executed or recommended as executable.

```text
Review the Rocketcart MCP output below for write-gate safety.

Check whether every bid, budget, placement, negative, pause, relaunch, or campaign-creation action:
1. Was not executed during the initial read-only review.
2. Has explicit human approval for the exact action row.
3. Includes exact entity IDs, not names alone.
4. Includes current value and proposed value.
5. Includes expected impact and primary risk.
6. Includes live preflight immediately before execution.
7. Includes readback after execution.
8. Includes 3-day, 7-day, and/or 14-day monitoring criteria.
9. Blocks execution when profile, IDs, current state, margin, inventory, Featured Offer / Buy Box, or confidence is missing.

Return:
- Pass / Needs revision / Fail.
- Any action that is not executable yet and why.
- Required preflight reads.
- Required approval text or decision.
- Required readback and monitoring.

Rocketcart output:
```
PASTE OUTPUT HERE
```
```
