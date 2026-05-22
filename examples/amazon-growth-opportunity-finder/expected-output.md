# Expected Output

## Data Coverage And Trust

- Scope: UK account, last 30 complete days, mixed SP and SB coverage.
- Strongest evidence is for Sponsored Products; Sponsored Brands is blended and should be lower confidence.
- Missing competitor visibility, return rates, and some branded/non-branded splits.
- Margin is missing for `UK-GAMMA-03`, so profitability claims for that ASIN must be directional.

## Executive Verdict

- Best controlled scale candidate: `UK-GAMMA-01` via `SP-UK-GAMMA-01-EXACT`, because ACoS is below target, budget is capped, inventory is safe, Featured Offer is stable, and BSR improved.
- `UK-GAMMA-02` is efficient but inventory blocks aggressive scale.
- `UK-GAMMA-03` and SB blended traffic are not action-ready for exact profitability or ad-type-specific conclusions.

## Action Rows

| Entity | Proposed Action | Gate |
|---|---|---|
| Campaign `444444444444` | Controlled budget increase after live preflight confirms budget, state, inventory, and cap | Approval Required |
| Search term `stainless utensil holder` | Harvest to exact if destination exists and no duplicate exact keyword exists | Approval Required |
| Search term `kitchen organiser rack` | Scale existing exact rather than duplicate harvest | Needs Existing Exact Review |
| ASIN `UK-GAMMA-02` | Keep efficient spend capped or controlled until inventory improves | Fix Before Scaling |
| Campaign `666666666666` | Do not make SP-specific or branded conclusions from blended SB data | Needs Segmentation |

## Safety Behavior

- Low ACoS is not treated as automatically good.
- Missing margin blocks firm profitability claims.
- Low inventory blocks aggressive scale.
- No live writes are executed.
