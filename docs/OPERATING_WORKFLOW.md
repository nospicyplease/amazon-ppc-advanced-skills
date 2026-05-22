# Operating Workflow

## Choose A Path

### Path A: Static-Export Workflow

Use this path when the user provides CSVs, pasted tables, screenshots, or summaries.

1. Confirm marketplace, account/profile, currency, timezone, ASIN/campaign scope, current window, and comparison window.
2. Map available exports to the relevant skill:
   - Performance drop: `amazon-ads-performance-drop-diagnosis`.
   - Growth review: `amazon-growth-opportunity-finder`.
   - Search-term harvest: `amazon-search-term-harvest-planner`.
   - Unified plan: `amazon-account-growth-operating-system`.
3. State missing data and confidence limits before recommendations.
4. Produce approval-ready action rows, not live writes.
5. Use examples, evals, and stress tests to review output quality.

Static exports can be stale. Any future live execution still requires approval, preflight, exact IDs, current/proposed values, readback, and monitoring.

### Path B: Rocketcart Live Ads + Product-Intelligence Workflow

Use this path when Rocketcart MCP is available.

1. Run `rocketcart-amazon-ads-live-review` as the single Rocketcart bridge skill.
2. Choose the review mode:
   - `Live Optimization Review` for current live account review and drift checks.
   - `Product-Aware Growth Review` for Grow / Fix Before Scaling / Protect / Monitor / Blocked classification.
   - `Preflight / Approval Readiness Review` for candidate action rows.
   - `Post-Change Readback / Monitoring Review` after approved changes.
3. Confirm profile. If multiple profiles match, do not assume; ask for selection.
4. Inspect live campaigns, product ads/ASIN mapping, budget changes, targeting or negative changes, live drift, and snapshots.
5. Inspect product intelligence where available: data freshness and quality, ASIN-level controls, category rank/BSR movement, price, estimated demand, rating/reviews, inventory or availability, Featured Offer / Buy Box, competitor signals, seasonality, and recent-change context.
6. Convert findings into classifications and proposed action rows.
7. Do not execute writes during the initial review.
8. Execute only after explicit approval, live preflight, exact entity IDs, current/proposed values, expected impact/risk, product-readiness checks, readback, and monitoring criteria.

If live state differs from an approved row, do not execute without refreshed approval.

## Full Account Review

Use this workflow for a weekly or monthly account review.

If Rocketcart MCP is available, `rocketcart-amazon-ads-live-review` can be used before finalizing actions to compare the plan against live Sponsored Products campaign state, product ads/ASIN mapping, product intelligence, recent budget changes, live drift, prior optimization context, and snapshots.

### Step 1: Establish Data Coverage And Freshness

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

- Data coverage map.
- Evidence thresholds.
- Commercial-impact score.
- Incrementality checks.
- Retail-readiness gates.
- Action rows.

### Optional Step 3b: Plan Search-Term Harvesting

Run or apply `amazon-search-term-harvest-planner` when search-term exports are available and the account needs exact-match harvesting, routing cleanup, or negative decisions.

Use it to:

- Classify search terms by harvest readiness, traffic type, strategic role, relevance, economics, and retail-readiness fit.
- Choose exact destination campaigns or mark `Needs Destination`.
- Check duplicate exact keywords, product targets, and existing negatives.
- Decide whether source negatives are safe, blocked, or need more data.
- Produce machine-readable action rows with write-readiness statuses: `PLANNING_ONLY`, `NEEDS_DATA`, `BLOCKED`, `APPROVAL_REQUIRED`, or `APPROVAL_READY`.
- Mark a row `APPROVAL_READY` only when exact profile, source, destination, keyword/target/negative IDs where applicable, current/proposed values, duplicate checks, current negative checks, destination feasibility, approval text, preflight checks, readback checks, and monitoring criteria are complete.

Do not add source negatives solely because a term was harvested. Preserve brand defense, own-ASIN defense, launch/rank-defense, profitable discovery, and low-sample strategic traffic unless waste or routing evidence is clear.

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

### Optional Step 4b: Run Rocketcart Live Ads + Product-Intelligence Review

Run or apply `rocketcart-amazon-ads-live-review` when Rocketcart MCP is available or when live Sponsored Products state may differ from static exports.

Use it to:

- Choose a review mode: `Live Optimization Review`, `Product-Aware Growth Review`, `Preflight / Approval Readiness Review`, or `Post-Change Readback / Monitoring Review`.
- Confirm the correct profile.
- Inspect current campaign budgets, states, bidding strategies, and placement modifiers.
- Map product ads to ASIN/SKU context.
- Check data freshness/quality and ASIN-level controls.
- Inspect product intelligence where available: category rank/BSR movement, BSR versus ads, price, estimated demand, rating/reviews, inventory or availability, Featured Offer / Buy Box, competitor signals, and seasonality.
- Detect budget changes.
- Detect keyword/target bid or state changes and negative changes when relevant.
- Detect live drift since optimization snapshots.
- Review previous snapshots, changelogs, entity history, pending evaluations, and cooldowns.
- Classify ASINs/campaigns/actions as `Grow`, `Fix Before Scaling`, `Protect`, `Monitor`, or `Blocked`.
- Convert the operating plan into exact action rows with entity IDs, current values, proposed values, preflight checks, approval status, readback checks, and monitoring windows.

Do not execute writes during this review. Treat it as the product-aware live-state bridge between analysis and approval.

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

1. Data coverage, quality, and freshness.
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

For Rocketcart MCP execution, every approved write also requires live preflight, exact entity IDs, current value, proposed value, expected impact, risk, readback, and monitoring criteria.
