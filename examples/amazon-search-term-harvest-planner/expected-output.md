# Expected Output

## Data Coverage And Harvest Gate

- Scope: US Sponsored Products, last 30 complete days.
- Search term, targeting map, existing exact keywords, existing negatives, and product readiness are available.
- Missing purchased-product report, organic rank, competitor movement, and full margin.

## Classification

| Search Term | Classification | Reason | Gate |
|---|---|---|---|
| `steel water bottle 1 liter` | Scale Existing Exact | Already exists as exact keyword `kw-100`; do not duplicate harvest | Needs Existing Exact Review |
| `delta bottle replacement lid` | Scale Existing Exact / Brand Defense | Existing exact keyword `kw-101`; do not add source negative without defense context | Approval Required |
| `competitor travel mug` | Negative Candidate | Spend with zero orders, but confirm relevance and existing negative scope first | Approval Required |
| `substitute asin b0example` | Product-Target Candidate / Own-ASIN Defense Check | Could be own-ASIN or substitute traffic; do not negative blindly | Needs Data |
| `steel bottle` | Watchlist | One order is low sample | Monitor |

## Safety Behavior

- Harvesting does not automatically create source negatives.
- Duplicate exact keywords are blocked.
- Brand defense and own-ASIN defense are preserved unless waste is isolated.
- No changes are executed.
