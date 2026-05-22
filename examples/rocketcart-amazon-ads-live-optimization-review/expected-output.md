# Expected Output

## Mode, Scope, And Data Coverage

- Mode: Rocketcart MCP when live capabilities are available; otherwise standalone simulation from fixtures.
- Profile: `example_de`.
- Initial review is read-only.
- Live reads/synthetic fixtures include campaigns, product ads/ASIN context, product intelligence, budget changes, drift from snapshot, and proposed action candidates.
- Missing full search terms, full BSR history, total retail sales, complete competitor data, and final approval.

## Executive Verdict

- `rc-camp-1001` has live budget drift from the latest snapshot and may be approval-ready for controlled budget increase only after preflight confirms current budget is still 40 EUR.
- `rc-camp-1001` maps to `DE-RC-CORE-01`, whose synthetic product gate is scale-candidate: inventory is safe, Featured Offer is stable, rating/reviews are strong, and competitor health is stable.
- `rc-camp-1002` maps to `DE-RC-RANK-02` and is blocked from scale because inventory is only 9 days of supply and competitor coupon risk exists.
- The negative keyword row is not executable because the exact entity ID and defensive-risk review are missing.

## Proposed Action Rows

| Entity | Current State | Proposed Action | Gate |
|---|---|---|---|
| Campaign `rc-camp-1001` / ASIN `DE-RC-CORE-01` | Budget 40 EUR, enabled; product gate scale-candidate | Increase to 55 EUR after live preflight | Approval Required, Not Executed |
| Campaign `rc-camp-1002` / ASIN `DE-RC-RANK-02` | Budget 30 EUR, 9 inventory days, competitor coupon risk | Do not increase budget | Blocked |
| Negative keyword | Missing ID and missing ASIN/defensive context | No execution | Needs IDs |

## Execution Gate

- Do not execute during the initial review.
- If live preflight shows a current value different from the approved row, do not execute and request refreshed approval.
- Any later write requires exact approval text, live preflight, current/proposed values, readback, and 3/7/14-day monitoring.
