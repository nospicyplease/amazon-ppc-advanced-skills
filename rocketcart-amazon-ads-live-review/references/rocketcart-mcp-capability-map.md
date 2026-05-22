# Rocketcart MCP Capability Map

Use this reference when Rocketcart MCP capabilities are available. The public skill should reason about capability categories rather than exposing implementation-specific names.

## Read Capabilities

### Profile And Live Ads State

- Profile discovery: list available Amazon Ads profiles with country, marketplace, and account context. Use first when the user did not specify a profile.
- Campaign state: inspect Sponsored Products campaigns, including budget, state, targeting type, bidding strategy, and placement modifiers.
- Product ads: inspect advertised ASIN/SKU mapping, product-ad state, campaign ID, and ad group ID.
- Bid guidance: inspect marketplace bid guidance for keyword or product-target candidates before proposing bid changes.

### Change And Recent-Action Context

- Budget changes: detect recent day-over-day campaign budget changes.
- Live drift: compare current live Ads state against the latest optimization snapshot.
- Targeting changes: detect keyword/target bid or state changes from recent snapshots.
- Negative changes: detect negative keyword additions, removals, or state changes.
- Snapshots and changelogs: inspect prior optimization snapshots and change logs.
- Entity history: inspect historical changes for a keyword, target, campaign, or other entity ID.

### Product Intelligence And Data Quality

Use available Rocketcart product-intelligence reads to inspect:

- Profile KPIs, campaign signals, budget/settings, waste, placement, ASIN performance, search terms, and report quality.
- ASIN-scoped KPI precision and mixed-ASIN risk before ASIN-scoped actions.
- Category rank/BSR movement, price, estimated demand, offer status, and freshness.
- Product metrics compared with Sponsored Products spend, sales, ACoS, and ROAS.
- Daily BSR alongside impressions, clicks, spend, sales, ACoS, and ROAS.
- BSR responsiveness, lag, momentum, and confounders before rank-support decisions.
- Seasonal BSR, demand, and price history when enough data exists.
- Competitor price, stock, Featured Offer / Buy Box, and deal changes.

## Write Capabilities

Never use write capabilities during the initial review. Use them only after explicit approval, live preflight, exact IDs, and a readback plan.

Write-capability families include:

- Campaign budget updates.
- Keyword bid updates.
- Product-target bid updates.
- Product-target pause or enable actions.
- Product-ad pause or enable actions.
- Placement modifier updates.
- Negative keyword creation or removal.
- Campaign creation or relaunch.

## Read Sequence

When the profile is missing:

- Use profile discovery.
- If exactly one profile matches, state the assumption before continuing.
- If multiple profiles plausibly match, ask the user to choose. Do not infer from country or name alone.

After profile confirmation:

- Inspect live campaign state.
- Inspect product ads and ASIN/SKU mapping.
- Inspect recent budget, targeting, negative, and placement changes.
- Inspect snapshots, changelogs, and entity history.
- Inspect product intelligence when ASIN context affects the decision.

## Review Mode Support

### Live Optimization Review

Use this mode to reconcile current Ads state against the user's goal or static findings.

- Confirm profile and marketplace.
- Inspect enabled Sponsored Products campaigns unless paused/archived context is requested.
- Compare current budgets, states, placement modifiers, targeting context, and recent changes against snapshots.
- Produce read-only findings and proposed action rows without execution.

### Product-Aware Growth Review

Use this mode when the decision depends on whether the product can safely absorb more traffic.

- Map campaigns and product ads to ASIN/SKU context.
- Inspect inventory or availability, Featured Offer / Buy Box, price, reviews/rating, estimated demand, category rank/BSR movement, competitor signals, margin or target economics, and recent product changes where available.
- Classify each material ASIN/campaign/action as `Grow`, `Fix Before Scaling`, `Protect`, `Monitor`, or `Blocked`.
- Block or downgrade scale when product context is missing or contradicts the PPC signal.

### Preflight / Approval Readiness Review

Use this mode when candidate rows already exist.

- Check exact entity IDs, current live values, proposed values, profile, marketplace, state, recent drift, product readiness, expected impact, risk, approval wording, readback, and monitoring.
- Mark each row as approval-ready only when all required fields and business gates are satisfied.
- If live state differs from the row's current value, return a refreshed row and request refreshed approval.

### Search-Term Harvest Review

Use `amazon-search-term-harvest-planner` for search-term-specific Rocketcart work. The same capability categories apply, with extra emphasis on:

- Resolving source campaign/ad group, destination campaign/ad group, keyword, target, negative, product-ad, ASIN, and profile IDs.
- Checking duplicate exact keywords and duplicate product targets before harvest.
- Checking current negatives that may block destination delivery or source traffic.
- Checking source-negative blast radius before negative exact or phrase actions.
- Checking destination budget/state and advertised ASIN fit before rerouting traffic.
- Blocking duplicate harvest when a live exact already exists; use delivery fix instead.
- Executing only exact approved row IDs, then reading back affected entities and monitoring traffic routing.

### Post-Change Readback / Monitoring Review

Use this mode after approved changes have been made or when the user asks whether changes worked.

- Read back affected entities and compare current state with the approved rows.
- Review early spend, delivery, ACoS/ROAS, orders, CVR, budget pacing, category rank/BSR movement, product readiness, and competitor changes.
- Classify outcomes as `Readback Confirmed`, `Partially Applied`, `Not Applied`, `Monitoring`, `Worked`, `Failed`, or `Needs More Data`.
- Recommend rollback or next-response only when evidence and approval gates support it.

## Preflight Basics

Preflight a write candidate by checking at least:

- Profile and marketplace.
- Exact campaign, ad group, keyword, target, product-ad, or negative ID as relevant.
- Current live state.
- Current value and proposed value.
- Recent budget, bid, placement, negative, or state drift.
- Inventory, availability, Featured Offer / Buy Box, margin, and strategic role.
- Product context when the action can affect product-level traffic, rank, launch, harvesting, or stock.

If any field differs from the approved row, the approval is stale.

## Preflight By Action Type

Budget change:

- Confirm profile, campaign ID, campaign state, current budget, current spend/pacing context, recent budget changes, and whether the campaign is strategically defensive or rank-supporting.
- Confirm product-ad ASIN/SKU mapping and product context when the campaign is ASIN-scoped or has mixed-ASIN risk.
- Block if inventory, availability, Featured Offer / Buy Box, margin, BSR, price, review/rating, competitor, or conversion risk makes the budget increase unsafe.

Keyword bid change:

- Confirm keyword ID, campaign/ad group, match type, current bid, current state, recent bid drift, performance evidence, and whether the term is branded, defensive, launch, rank-supporting, or exploratory.
- Confirm product context for the advertised ASIN when the bid change is meant to drive product-level sales, BSR, or launch velocity.
- Block if sample size is weak or the proposed change depends on missing margin, inventory, availability, or retail readiness.

Placement modifier change:

- Confirm campaign ID, current placement modifiers, placement performance, CPC/CVR difference, recent placement drift, and strategic role.
- Block if placement data is too thin, the campaign mixes incompatible traffic types, or product context makes additional traffic unsafe.

Negative keyword creation:

- Confirm search term, match type, campaign ID, ad group ID when ad-group-level, current waste evidence, relevance, and strategic role.
- Confirm advertised ASIN, purchased-product or product-target context when available.
- Block if the term could be brand defense, own-ASIN defense, launch/rank defense, competitor conquesting with strategic value, or a profitable low-volume term.

Negative deletion:

- Confirm negative keyword ID, current negative scope, reason to restore traffic, and risk of reopening waste.

Campaign creation:

- Confirm campaign objective, advertised ASINs, SKU/product-ad mapping, product intelligence, budgets, bids, targeting, negatives, portfolio, naming, launch state, and retail-readiness gates.
- Prefer a validation-only check before any real creation when the environment supports it.

Product-ad or target state change:

- Confirm product ad ID or target ID, ASIN/SKU, current state, performance evidence, product readiness, and strategic role.
- Block if the change could harm active winners, brand defense, own-ASIN defense, rank support, or a product with unresolved mixed-ASIN contamination.

## Readback

After an approved write, read back the affected entity:

- Campaign budget or state.
- Product-ad state.
- Placement modifiers.
- Live drift from snapshot when useful.
- Negative creation/deletion or keyword/target bid state where the host environment exposes those reads.

Report what changed, what did not change, and what must be monitored over 3, 7, and 14 days.

## Failure Modes

Profile ambiguity:

- If multiple profiles match the user's request, list the candidates and ask the user to pick one.
- Do not inspect or execute against a guessed profile.

Missing IDs:

- Campaign names, keyword text, and search terms are not enough for live writes.
- Classify the row as `Needs IDs` until the exact Amazon Ads entity IDs are known.

Stale snapshot or changelog:

- Treat old snapshots as context, not approval.
- Refresh live state before any execution decision.

Current value mismatch:

- If live preflight shows a current bid, budget, placement modifier, negative state, or campaign state that differs from the approved row, do not execute.
- Produce a refreshed row and request refreshed approval for the new current/proposed pair.

Validation failure:

- Treat validation errors as blockers until resolved.
- Report the error, affected entity, likely cause, and the safest next read or edit.

Validation passes but business gate fails:

- Technical validation does not override inventory, Featured Offer / Buy Box, margin, or brand/rank-defense gates.
- Keep the row blocked or downgrade it to a controlled test when business risk is high.

Write capability available during initial review:

- Availability is not permission.
- Do not use write capabilities during initial review even when they are exposed in the environment.

Product intelligence unavailable:

- State which product context is unavailable.
- Lower confidence and block or downgrade scale, launch, pause, negative, or rank-support recommendations when the missing context could change the decision.

Mixed-ASIN contamination:

- If a campaign or ad group contains multiple ASINs and ASIN-level performance cannot be isolated, do not make broad campaign-level pause, budget, bid, or negative decisions.
- Use product-ad and ASIN-level control reads where available.
