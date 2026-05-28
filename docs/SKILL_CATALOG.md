# Skill Catalog

If you are new to the project, start with [FAQ](FAQ.md). The fastest rule is: use the narrowest skill that matches the job, then use `amazon-account-growth-operating-system` to combine findings into a prioritized plan.

## Decision Matrix

| User situation | Start with | Minimum useful data | Why | Main safety blocker |
|---|---|---|---|---|
| Sales, orders, ROAS, TACoS, BSR, CVR, rank, or traffic worsened | `amazon-ads-performance-drop-diagnosis` | Current and baseline windows, campaign metrics, total sales if TACoS matters, BSR, retail readiness, change history | Diagnose the break before changing controls | Missing comparison windows, BSR, total sales, retail readiness, or change history |
| No obvious drop, want profitable upside | `amazon-growth-opportunity-finder` | Campaign/targeting/search-term data, economics or target ACoS, inventory, Featured Offer / Buy Box, total sales if incrementality matters | Finds safe scale, harvest, budget, ASIN, and placement opportunities | Missing margin, inventory, total sales, search terms, or retail readiness |
| Need one weekly account action plan | `amazon-account-growth-operating-system` | Drop findings, growth findings, or raw account data with scope, economics, readiness, and rank context | Prioritizes protect/grow/fix/monitor into one queue | Conflicting upstream findings or unresolved high-confidence downside risk |
| Search-term cleanup, exact harvesting, or Rocketcart live harvest preflight | `amazon-search-term-harvest-planner` | Search term report, targeting/keyword map, destination structure, existing exact/negatives, destination feasibility, economics/readiness; Rocketcart profile and live state when available | Separates harvest, route, negative, bid-down, watchlist, live preflight, execution, and readback decisions with write-readiness statuses | Missing source/destination map, exact keyword map, current negative map, destination feasibility, live profile, exact IDs, or strategic-role context |
| Rocketcart live Amazon Ads + product-intelligence review | `rocketcart-amazon-ads-live-review` | Rocketcart profile, live campaigns, product ads/ASIN mapping, category/BSR movement, product context, budget changes, snapshots, action goal | Compares analysis to live Ads state, product readiness, product intelligence, and recent-change context before proposing approval-gated rows | Missing profile, product context, exact IDs, live preflight, approval, or readback |
| Public, demo, or recording-safe optimization output | `case-camouflage-skill` | Source data in private context, tenant-scoped registry, HMAC secret for text-only identifiers, output destination | Preserves exact KPIs and source-plane optimization logic while masking display labels and producing approval packets only | Missing masking registry, HMAC secret, leakage scan, private manifest path, or real-profile dry-run validation |

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
- Running Rocketcart Live Harvest Review, Preflight / Approval Readiness Review, Execute Approved Rows, or Post-Change Readback / Monitoring Review for search-term-specific actions.
- Separating brand defense, own-ASIN defense, launch/rank-defense, category generic, competitor, and exploratory traffic.
- Producing machine-readable, approval-gated action rows for harvesting and routing.

Key outputs:

- Data coverage and harvest gate.
- Executive summary.
- Search term classification table.
- Harvest action rows.
- Rocketcart live context section when live reads are used: profile, exact ID resolution, recent drift, product context, and live limitations.
- Write-readiness status for each row: `PLANNING_ONLY`, `NEEDS_DATA`, `BLOCKED`, `APPROVAL_REQUIRED`, or `APPROVAL_READY`.
- Approval, execution, readback, and monitoring status for Rocketcart-mode rows.
- Negative and routing decisions.
- Blocked/watchlist terms.
- Monitoring plan.
- Missing data and next pulls.

Important guardrail:

Do not add source negatives just because a term was harvested. Source negatives require safe routing or waste evidence and must not cut brand defense, own-ASIN defense, launch/rank-defense, profitable discovery, or low-sample strategic traffic. No row is `APPROVAL_READY` without exact IDs, current/proposed values, duplicate checks, current negative checks, destination feasibility, approval text, preflight, readback, and monitoring. In Rocketcart MCP mode, connection availability is not approval; execution still requires exact row-level approval, live preflight, readback, and monitoring.

## 5. Rocketcart Amazon Ads Live Review

Folder: `rocketcart-amazon-ads-live-review`

Use when the operator wants a read-first Amazon Sponsored Products optimization review that can run from static exports or use Rocketcart MCP as the Amazon Ads + product-intelligence connection.

Best for:

- Live Optimization Review: current account review, live drift checks, and safer optimization recommendations.
- Product-Aware Growth Review: deciding what to Grow, Fix Before Scaling, Protect, Monitor, or Blocked using Ads and product context together.
- Preflight / Approval Readiness Review: checking whether candidate action rows have exact IDs, current values, product gates, approval text, readback, and monitoring.
- Post-Change Readback / Monitoring Review: confirming approved changes and monitoring early outcomes.
- Inspecting live Sponsored Products campaigns before proposing changes.
- Mapping product ads to ASIN/SKU context.
- Checking product intelligence such as category rank/BSR movement, price, estimated demand, rating/reviews, inventory or availability, Featured Offer / Buy Box, competitor signals, and BSR responsiveness where available.
- Listing Rocketcart profiles when the target profile is unknown.
- Detecting recent budget changes.
- Detecting live drift since the latest optimization snapshot.
- Reviewing snapshots and changelogs before recommending actions.
- Producing exact, approval-gated action rows.

Key outputs:

- Mode, scope, and data coverage.
- Executive verdict.
- Live state and change review.
- Product intelligence and readiness review.
- Product-aware classifications: `Grow`, `Fix Before Scaling`, `Protect`, `Monitor`, and `Blocked`.
- Read-only findings.
- Proposed action rows.
- Execution gate.
- Readback and monitoring plan.
- Missing data and next reads.

Important guardrail:

This skill does not execute writes by default. Bid, budget, placement, negative, pause, relaunch, or campaign-creation actions require explicit approval, live preflight, exact entity IDs, expected impact and risk, readback, and monitoring.

## 6. Case Camouflage Skill

Folder: `skills/case-camouflage-skill`

Use when Amazon Ads optimization output must be safe for public repos, demos, recordings, user-facing summaries, or eval artifacts while preserving exact metrics and real recommendation logic.

Best for:

- Masking account, profile, product, ASIN, SKU, campaign, ad group, keyword, search-term, target, placement, filename, URL, and source-derived identifiers.
- Keeping analytical grouping/ranking on raw source IDs before display masking.
- Building masked approval packets with immutable non-sensitive action IDs.
- Keeping raw execution payloads in private manifests for a separate approved execution tool.
- Scanning artifacts, logs, metadata, hidden sheets, rationales, and readbacks before release.

Key outputs:

- Masked diagnostics with exact KPIs.
- Masked approval packet rows.
- Private manifest boundary.
- Registry coverage summary with counts only.
- Leakage scan result.
- Production readiness report.

Important guardrail:

Never alter KPIs for privacy and never execute Amazon Ads changes from this skill.

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
- Standalone post-change learning review.
- Rocketcart approval-action verifier.

See [../ROADMAP.md](../ROADMAP.md) for scoped good-first-skill ideas.
