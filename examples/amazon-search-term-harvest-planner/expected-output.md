# Expected Output

## Data Coverage And Harvest Gate

- Scope: US Sponsored Products, last 30 complete days.
- Search term, targeting map, existing exact keywords, current negatives, destination state, budget status, and product readiness are available.
- Missing purchased-product report, organic rank, competitor movement, full margin, and some ASIN relationship context.
- No row is executable. `APPROVAL_READY` requires exact IDs, current/proposed values, duplicate checks, current negative checks, destination feasibility, approval text, preflight, readback, and monitoring.

## Rocketcart Live Context

- Mode: Rocketcart MCP capable, Live Harvest Review.
- Profile: `example_us`; marketplace and currency confirmed from live profile context.
- Live reads used: current campaign/ad group states, product-ad ASIN/SKU mapping, existing exact keywords, current negatives, destination budget status, recent drift, and product-readiness context from the synthetic fixture.
- Live limitation: purchased-product relationship data is still missing, so ASIN-like queries remain `NEEDS_DATA`.
- Execution: no rows executed. Execution would require exact row approval, live preflight with matching current values, readback, and monitoring.

## Classification

| Search Term | Classification | Write Readiness | Reason | Gate |
|---|---|---|---|---|
| `steel water bottle 1 liter` | Scale Existing Exact / Delivery Fix | BLOCKED | Existing exact keyword `kw-100` is paused; do not duplicate harvest | Reactivate/review existing exact after approval and preflight |
| `delta bottle replacement lid` | Scale Existing Exact / Brand Defense | APPROVAL_REQUIRED | Brand-defense exact keyword `kw-101` exists; source negative could cut defense | No source negative without approved defense routing |
| `competitor travel mug` | Bid Down / Keep Learning | APPROVAL_REQUIRED | High ACoS/zero orders, but campaign role is competitor conquest | Avoid automatic negative until strategic role and target CPA are confirmed |
| `substitute asin b0example` | Product-Target Candidate / Own-ASIN Defense Check | NEEDS_DATA | Could be own-ASIN or substitute traffic; destination missing | Needs ASIN relationship and destination IDs |
| `steel bottle` | Controlled Test | PLANNING_ONLY | One order is low sample | Controlled exact test or watchlist, not Harvest Ready |
| `delta steel bottle` | Harvest Ready but Destination Blocked | BLOCKED | Good volume, but exact destination is budget-starved | Resolve budget feasibility before approval |
| `kids steel water bottle` | Harvest Ready but Negative Conflict | BLOCKED | Destination has exact negative `neg-201` blocking delivery | Remove/resolve negative only after approval and preflight |
| `water bottle straw replacement` | Negative Candidate | APPROVAL_REQUIRED | Zero orders and irrelevant query family | Negative phrase requires blast-radius review; narrower negative exact may be safer |
| `insulated kids bottle` | Launch / Rank Controlled Test | PLANNING_ONLY | High ACoS is intentional only if launch/rank goal and stop-loss are explicit | Monitor rank objective, stock, and stop-loss |
| `steel bottle` from SB | Needs Ad-Type Separation | NEEDS_DATA | SB data is blended with SP term logic | Do not apply SP-only product-target or source-negative logic blindly |

## Example Action Rows

| row_id | mode | action_type | search_term_normalized | classification | write_readiness | approval_status | execution_status | source_ids | destination_ids | current_value | proposed_value | duplicate_check | current_negative_check | live_preflight_status | destination_feasibility | approval_text |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H-001 | Rocketcart Live Harvest Review | delivery_fix | `steel water bottle 1 liter` | Scale Existing Exact / Delivery Fix | BLOCKED | not_approvable | not_executed | `camp-100` / `ag-100` | existing exact `kw-100` | keyword paused | review/reactivate existing exact after preflight | Existing exact paused | clear | failed: duplicate exact exists | not ready until state/bid reviewed | Review existing exact; do not create duplicate |
| H-002 | Rocketcart Live Harvest Review | harvest_exact | `kids steel water bottle` | Harvest Ready but Negative Conflict | BLOCKED | not_approvable | not_executed | `camp-102` / `ag-102` | `camp-997` / `ag-997` | destination negative `neg-201` blocks term | remove blocker first, then review exact harvest | no duplicate exact found | blocked by `neg-201` | failed: destination negative conflict | blocked | Resolve negative conflict before approval |
| H-003 | Rocketcart Live Harvest Review | negative_exact_review | `water bottle straw replacement` | Negative Candidate | APPROVAL_REQUIRED | needs_explicit_approval | not_executed | `camp-103` / `ag-103` | none | source query active | proposed narrow negative exact after blast-radius review | not applicable | source negative family exists | required immediately before execution | not applicable | Approve only a narrow negative after blast-radius review |
| H-004 | Rocketcart Live Harvest Review | controlled_test | `steel bottle` | Controlled Test | PLANNING_ONLY | not_approvable | not_executed | `camp-104` / `ag-104` | `camp-997` / `ag-997` | one order, low sample | low-bid controlled test or watchlist | no duplicate exact found | clear | not required for planning row | feasible | Planning only; one order is not enough for approval-ready harvest |

## Safety Behavior

- Harvesting does not automatically create source negatives.
- Duplicate exact keywords are blocked.
- Brand defense and own-ASIN defense are preserved unless waste is isolated.
- Existing exact paused means delivery repair, not duplicate harvest.
- Budget-starved destinations and current negative conflicts block `APPROVAL_READY`.
- One-order winners remain controlled tests or watchlist.
- Mixed SP/SB data requires ad-type separation.
- No changes are executed.
- Rocketcart live context can make a static harvest row stale or blocked when duplicate exacts, negative conflicts, budget starvation, product-readiness issues, or current-value mismatches appear.
- Even `APPROVAL_READY` rows need a separate approval message naming exact row IDs before execution.
