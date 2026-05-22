# Skill Catalog

If you are new to the project, start with [FAQ](FAQ.md). The fastest rule is: use the narrowest skill that matches the job, then use `amazon-account-growth-operating-system` to combine findings into a prioritized plan.

## Decision Matrix

| User situation | Start with | Minimum useful data | Why | Main safety blocker |
|---|---|---|---|---|
| Sales, orders, ROAS, TACoS, BSR, CVR, rank, or traffic worsened | `amazon-ads-performance-drop-diagnosis` | Current and baseline windows, campaign metrics, total sales if TACoS matters, BSR, retail readiness, change history | Diagnose the break before changing controls | Missing comparison windows, BSR, total sales, retail readiness, or change history |
| No obvious drop, want profitable upside | `amazon-growth-opportunity-finder` | Campaign/targeting/search-term data, economics or target ACoS, inventory, Featured Offer / Buy Box, total sales if incrementality matters | Finds safe scale, harvest, budget, ASIN, and placement opportunities | Missing margin, inventory, total sales, search terms, or retail readiness |
| Need one weekly account action plan | `amazon-account-growth-operating-system` | Drop findings, growth findings, or raw account data with scope, economics, readiness, and rank context | Prioritizes protect/grow/fix/monitor into one queue | Conflicting upstream findings or unresolved high-confidence downside risk |
| Search-term cleanup or exact harvesting | `amazon-search-term-harvest-planner` | Search term report, targeting/keyword map, destination structure, existing exact/negatives, economics/readiness | Separates harvest, route, negative, bid-down, and watchlist decisions | Missing source/destination map, exact keyword map, or strategic-role context |
| Rocketcart live Sponsored Products review | `rocketcart-amazon-ads-live-optimization-review` | Rocketcart profile, live campaigns, budget changes, snapshots, action goal | Compares analysis to live state and proposes approval-gated rows | Missing profile, exact IDs, live preflight, approval, or readback |

## 1. Amazon Ads Performance Drop Diagnosis

Folder: `amazon-ads-performance-drop-diagnosis`

Use when performance is worse and the operator needs to know why.

Best for:

- Sales, orders, ROAS, ACoS, TACoS, profit, BSR, rank, traffic, CTR, CPC, or CVR decline.
- Identifying break dates and control changes.
- Diagnosing whether ads, retail readiness, competitors, inventory, price, reviews, or BSR moved first.
- Ranking biggest losers by business impact.
- Creating recovery actions only when evidence gates are met.

Key outputs:

- Data reliability and actionability gate.
- Executive verdict.
- Drop timeline.
- Impact summary table.
- Root-cause diagnosis.
- Biggest losers.
- BSR and competitor interpretation.
- Recommended recovery actions.
- Verification plan.

Important guardrail:

Do not recommend bid, budget, negative, pause, or relaunch execution unless the diagnostic action gate supports it.

## 2. Amazon Growth Opportunity Finder

Folder: `amazon-growth-opportunity-finder`

Use when the operator wants to find upside.

Best for:

- Profitable ASINs, campaigns, keywords, search terms, product targets, and placements to scale.
- Search term harvesting.
- Budget-capped winners.
- Underfunded ASINs.
- Good-BSR products with low ad support.
- Product targeting and rank-growth opportunities.
- Retail-readiness blockers that must be fixed before scaling.

Key outputs:

- Executive summary.
- Data coverage and trust.
- Top growth opportunities table.
- Ads-wise findings.
- BSR-wise findings.
- ASIN-level recommendations.
- Campaign and keyword actions.
- Budget reallocation plan.
- Watchlist.
- Questions and missing data.

Important guardrail:

Do not treat low ACoS as automatically good. Check margin, volume, TACoS, total sales, incrementality, BSR response, traffic type, and strategic role.

## 3. Amazon Account Growth Operating System

Folder: `amazon-account-growth-operating-system`

Use when the operator needs one prioritized account action plan.

Best for:

- Combining downside risks and upside opportunities.
- Deciding what to do first.
- Protecting current sales, BSR, rankings, and profit.
- Deciding which ASINs are safe to push.
- Blocking risky scale until retail-readiness issues are fixed.
- Reallocating budget from isolated waste to validated winners.
- Flagging human approval requirements.
- Defining success/failure criteria for every major action.

Key outputs:

- Executive decision summary.
- Single prioritized action queue.
- Protect list.
- Growth list.
- Fix-before-scaling list.
- Budget reallocation plan.
- Weekly operating plan.
- Monitoring rules.
- Human approval required.
- Missing data and confidence notes.

Important guardrail:

The Growth Operating System must preserve the downside skill's actionability gates and the upside skill's evidence thresholds. It should not average conflicting recommendations. It should resolve conflicts by protecting downside first.

## 4. Amazon Search Term Harvest Planner

Folder: `amazon-search-term-harvest-planner`

Use when the operator wants to mine Amazon Ads search terms for exact-match harvesting, controlled tests, source-negative routing, product-target expansion, bid-downs, or watchlist decisions.

Best for:

- Finding search terms ready for exact-match harvesting from auto, broad, phrase, or discovery campaigns.
- Choosing safe destination campaigns and ad groups.
- Avoiding duplicate exact keywords or product targets.
- Deciding whether source negatives are justified.
- Separating brand defense, own-ASIN defense, launch/rank-defense, category generic, competitor, and exploratory traffic.
- Producing approval-gated action rows for harvesting and routing.

Key outputs:

- Data coverage and harvest gate.
- Executive summary.
- Search term classification table.
- Harvest action rows.
- Negative and routing decisions.
- Blocked/watchlist terms.
- Monitoring plan.
- Missing data and next pulls.

Important guardrail:

Do not add source negatives just because a term was harvested. Source negatives require safe routing or waste evidence and must not cut brand defense, own-ASIN defense, launch/rank-defense, profitable discovery, or low-sample strategic traffic.

## 5. Rocketcart Amazon Ads Live Optimization Review

Folder: `rocketcart-amazon-ads-live-optimization-review`

Use when the operator wants a read-first Amazon Sponsored Products optimization review that can run from static exports or use Rocketcart MCP live reads.

Best for:

- Inspecting live Sponsored Products campaigns before proposing changes.
- Listing Rocketcart profiles when the target profile is unknown.
- Detecting recent budget changes.
- Detecting live drift since the latest optimization snapshot.
- Reviewing snapshots and changelogs before recommending actions.
- Producing exact, approval-gated action rows.

Key outputs:

- Mode, scope, and data trust.
- Executive verdict.
- Live state and change review.
- Read-only findings.
- Proposed action rows.
- Execution gate.
- Readback and monitoring plan.
- Missing data and next reads.

Important guardrail:

This skill does not execute writes by default. Bid, budget, placement, negative, pause, relaunch, or campaign-creation actions require explicit approval, live preflight, exact entity IDs, expected impact and risk, readback, and monitoring.

## Adding More Skills

Use `templates/amazon-ppc-skill-template/` when adding a new skill. New skills should usually be specialist workflows that can feed into `amazon-account-growth-operating-system`.

Good next categories:

- Wasted-spend triage.
- Budget reallocation.
- Inventory-aware scaling.
- BSR/rank rescue.
- Placement optimization.
- Brand-defense audit.
- Product-target expansion.
- Launch-readiness PPC planning.
- Rocketcart post-change monitoring.
- Rocketcart approval-action verifier.

See [../ROADMAP.md](../ROADMAP.md) for scoped good-first-skill ideas.
