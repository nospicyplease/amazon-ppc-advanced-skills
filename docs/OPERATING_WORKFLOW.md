# Operating Workflow

## Full Account Review

Use this workflow for a weekly or monthly account review.

### Step 1: Establish Data Trust

Collect or state missing:

- Marketplace, profile/account, currency, timezone.
- ASIN, campaign, and ad type scope.
- Exact current and comparison windows.
- Amazon Ads data by SP, SB, and SD where available.
- Total sales and orders for TACoS and incrementality.
- BSR history by ASIN and category.
- Inventory, Featured Offer / Buy Box, price, reviews, rating, delivery promise, listing changes, and suppression status.
- Change history for bids, budgets, placements, negatives, product ads, campaigns, portfolios, and automation.

Use T-1 windows when same-day data may be incomplete.

### Step 2: Diagnose Downside

Run or apply `amazon-ads-performance-drop-diagnosis`.

Answer:

- What broke?
- When did it break?
- Which entities created the loss?
- What is the likely cause?
- Is the recommendation action-safe?
- What must be protected before any growth push?

Carry forward:

- Actionability gate.
- Exact windows.
- Break timeline.
- Biggest losers.
- Root-cause confidence.
- Action gates.
- Verification plan.

### Step 3: Identify Upside

Run or apply `amazon-growth-opportunity-finder`.

Answer:

- Which ASINs, campaigns, keywords, search terms, targets, placements, or BSR movements deserve more investment?
- Which opportunities are blocked by inventory, Featured Offer / Buy Box, margin, conversion, reviews, listing, or price?
- Which campaigns are efficient but not incremental?
- Which search terms should be harvested?
- Which waste can fund growth without damaging rank, launch velocity, or defense?

Carry forward:

- Data source map.
- Evidence thresholds.
- Commercial-impact score.
- Incrementality checks.
- Retail-readiness gates.
- Action rows.

### Step 4: Orchestrate The Account

Run or apply `amazon-account-growth-operating-system`.

Classify every finding:

- `Protect`: risk to revenue, BSR, profit, or account stability.
- `Grow`: validated and retail-ready upside.
- `Fix Before Scaling`: upside exists but scale is blocked.
- `Monitor`: promising or concerning, but not action-ready.

Resolve conflicts:

- High-confidence protect findings override scale.
- Readiness blockers convert scale into fix-before-scale.
- Branded/defensive efficiency requires incrementality evidence before expansion.
- Low-confidence downside adds monitoring rather than blocking reversible high-confidence growth.
- Waste can fund growth only when isolated and not strategically protective.

### Step 5: Build The Action Queue

Every major action should include:

- Priority score.
- ASIN, campaign, keyword, search term, or target.
- Action type.
- Reason.
- Expected impact.
- Risk.
- Confidence.
- Timing.
- Whether human approval is required.

### Step 6: Monitor And Learn

For every major action define:

- Metrics to watch.
- Time window.
- Success condition.
- Failure condition.
- Next response.

Typical windows:

- 3 days: early spend, delivery, and obvious breakage.
- 7 days: early ACoS, CVR, orders, and BSR response.
- 14 days: performance validation and budget adjustment.
- 30 days: TACoS, BSR, organic sales, profitability, and strategic direction.

## Daily Short Workflow

Use the short workflow when the operator only needs a daily action plan:

1. Data trust and freshness.
2. Top 3 protect risks.
3. Top 3 growth actions.
4. Top 3 fix-before-scale blockers.
5. Budget movement.
6. Approval required.
7. Monitoring triggers.

## Approval Rules

Require approval for:

- Large budget increases.
- Major bid increases.
- Pausing high-revenue or rank-defensive campaigns.
- Aggressive ranking campaigns.
- Structural campaign rebuilds.
- Actions on low-margin products.
- Actions during inventory or Featured Offer / Buy Box risk.
- Product-level strategy changes.
- Brand-defense reductions.
- Competitor attack expansion.
- Low-confidence recommendations.

