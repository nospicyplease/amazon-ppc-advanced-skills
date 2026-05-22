# Expected Output

## Mode, Scope, And Data Coverage

- Mode: Rocketcart MCP when live capabilities are available; otherwise standalone simulation from fixtures.
- Review mode: Product-Aware Growth Review.
- Profile: `example_de`.
- Initial review is read-only.
- Live reads/synthetic fixtures include campaigns, product ads/ASIN context, product intelligence, budget changes, drift from snapshot, and proposed action candidates.
- Missing full search terms, full BSR history, total retail sales, complete competitor history, product context for `rc-camp-1006`, and final approval.

## Executive Verdict

- `rc-camp-1001` has live budget drift from the latest snapshot and may be approval-ready for controlled budget increase only after preflight confirms current budget is still 40 EUR.
- `rc-camp-1001` maps to `DE-RC-CORE-01`, whose synthetic product gate is scale-candidate: inventory is safe, Featured Offer is stable, rating/reviews are strong, and competitor health is stable.
- `rc-camp-1002` maps to `DE-RC-RANK-02` and is blocked from scale because inventory is only 9 days of supply and competitor coupon risk exists.
- `rc-camp-1003` maps to `DE-RC-CAT-03`; BSR improved, but category-wide improvement and competitor stockout signal make ads-to-BSR causality unsupported. Monitor rather than scaling.
- `rc-camp-1004` maps to `DE-RC-REV-04` and should be Fix Before Scaling because rating is 3.7 with only 18 reviews.
- `rc-camp-1005` maps to `DE-RC-PRICE-05` and should be Protect or Monitor because a competitor price drop makes scale risky until price/margin response is reviewed.
- `rc-camp-1006` is blocked from product-level scale because product context is unavailable.
- The negative keyword row is not executable because the exact entity ID and defensive-risk review are missing.

## Product-Aware Classification

| Campaign / ASIN | Classification | Product Context | Decision |
|---|---|---|---|
| `rc-camp-1001` / `DE-RC-CORE-01` | Grow | 45 inventory days, Featured Offer stable, rating 4.6, 520 reviews, stable competitors | Controlled budget increase can be approval-ready after live preflight. |
| `rc-camp-1002` / `DE-RC-RANK-02` | Blocked | 9 inventory days and competitor coupon risk | No scale; protect stock and monitor. |
| `rc-camp-1003` / `DE-RC-CAT-03` | Monitor | BSR improved 14%, but category-wide improvement and competitor stockout confound the signal | Do not credit Ads as the proven BSR driver; hold budget and gather more evidence. |
| `rc-camp-1004` / `DE-RC-REV-04` | Fix Before Scaling | Rating 3.7 and 18 reviews | Improve conversion/social proof before adding traffic. |
| `rc-camp-1005` / `DE-RC-PRICE-05` | Protect | Competitor price dropped 12% and BSR worsened | Avoid scaling into a weaker price position; review margin/price response. |
| `rc-camp-1006` / unknown ASIN | Blocked | Product context unavailable | Needs ASIN/SKU, inventory, offer, price, reviews, margin, and competitor context before product-level actions. |

## Proposed Action Rows

| Entity | Current State | Proposed Action | Classification | Gate |
|---|---|---|---|---|
| Campaign `rc-camp-1001` / ASIN `DE-RC-CORE-01` | Budget 40 EUR, enabled; product gate scale-candidate | Increase to 55 EUR after live preflight | Grow | Approval Required, Not Executed |
| Campaign `rc-camp-1002` / ASIN `DE-RC-RANK-02` | Budget 30 EUR, 9 inventory days, competitor coupon risk | Do not increase budget | Blocked | Blocked |
| Campaign `rc-camp-1003` / ASIN `DE-RC-CAT-03` | Budget 50 EUR, BSR improved but confounded | Hold budget and monitor | Monitor | Monitor Only |
| Campaign `rc-camp-1004` / ASIN `DE-RC-REV-04` | Budget 25 EUR, weak reviews/rating | No scale until product readiness improves | Fix Before Scaling | Blocked Until Fixed |
| Campaign `rc-camp-1005` / ASIN `DE-RC-PRICE-05` | Budget 45 EUR, competitor price pressure | No budget increase until price/margin risk is reviewed | Protect | Monitor Or Protect |
| Campaign `rc-camp-1006` / unknown ASIN | Budget 20 EUR, product context unavailable | No product-level scale | Blocked | Needs Data |
| Negative keyword | Missing ID and missing ASIN/defensive context | No execution | Blocked | Needs IDs |

## Execution Gate

- Do not execute during the initial review.
- If live preflight shows a current value different from the approved row, do not execute and request refreshed approval.
- Any later write requires exact approval text, live preflight, current/proposed values, readback, and 3/7/14-day monitoring.
