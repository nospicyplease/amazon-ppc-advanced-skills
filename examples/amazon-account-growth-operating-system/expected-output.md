# Expected Output

## Data Coverage And Trust

- Scope: DE account, last 14 complete days versus prior 14 days with 30-day context.
- Uses upstream drop and growth findings plus supporting account context.
- Missing competitor price movement, full bid history, organic rank, exact margin for one child ASIN, and purchased-product leakage.

## Executive Decision

- Protect `SP-DE-ORG-01-EXACT` first because it is tied to recent revenue and BSR deterioration.
- Grow `SP-DE-ORG-03-EXACT` only after preserving recovery budget and live preflight.
- Do not scale `DE-ORG-02` aggressively until inventory improves.
- Do not add negatives for ambiguous defensive traffic.

## Prioritized Queue

| Priority | Class | Entity | Action | Gate |
|---|---|---|---|---|
| 1 | Protect | Campaign `777777777777` | Investigate coupon/budget/Top of Search recovery and prepare approval-gated budget restoration if live state matches | Approval Required |
| 2 | Fix Before Scaling | ASIN `DE-ORG-02` | Resolve inventory constraint before scale | Blocked |
| 3 | Grow | Campaign `999999999999` | Controlled budget increase only if protect budget is not compromised | Approval Required |
| 4 | Monitor | `term-unmapped-01` | Do not negative until defensive role is disproven | Needs Data |

## Safety Behavior

- Conflicting findings are resolved by protecting downside first.
- No action is executable without exact IDs, current/proposed values, approval, preflight, readback, and monitoring.
- Missing data lowers confidence rather than being hidden.
