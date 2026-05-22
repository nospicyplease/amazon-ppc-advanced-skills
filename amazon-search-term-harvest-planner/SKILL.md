---
name: amazon-search-term-harvest-planner
description: Find Amazon Ads search terms ready for exact-match harvesting from auto, broad, phrase, or other discovery campaigns. Use when Codex needs to classify search terms by harvest readiness, choose safe destination campaigns/ad groups, decide whether source negatives are justified, and produce deterministic planning or approval-gated Sponsored Products or Sponsored Brands action rows without unsafe negatives, duplicate routing, brand-defense cuts, own-ASIN-defense cuts, launch/rank mistakes, or low-sample overfitting.
---

# Amazon Search Term Harvest Planner

## Purpose

Turn Amazon Ads search term data into a safe, specific harvesting plan. Identify search terms that deserve exact-match isolation, product-target expansion, bid direction, destination routing, or watchlist treatment. Do not treat every converting query as harvest-ready, and do not add source negatives unless routing or waste evidence supports it.

Optimize for clean traffic control, profitable growth, and learning. Preserve brand defense, own-ASIN defense, launch/rank-defense traffic, and strategically valuable discovery until the data proves a safer route.

This is a standalone planning skill by default. It may prepare approval-ready rows, but it must not create keywords, negatives, product targets, bids, budgets, or campaigns.

## Required Inputs

Gather, derive, or mark unavailable:

- Marketplace, profile/account, currency, timezone, ad type, and date windows.
- Search term report with campaign, ad group, search term, match type/source targeting where available, impressions, clicks, spend, orders, sales, ACoS/ROAS, CPC, CTR, and CVR.
- Targeting or keyword report with existing keywords/targets, match type, bids, states, and campaign/ad group destinations.
- Campaign and ad group structure: targeting type, naming, budgets, states, portfolio, advertised ASINs, and strategic role.
- Product context: advertised ASIN, purchased ASIN where available, parent/child relationship, category, price, margin or target ACoS/CPA, inventory, Featured Offer / Buy Box, reviews, rating, delivery promise, and listing readiness.
- Traffic segmentation: branded, own-brand generic, category generic, competitor brand, competitor ASIN, own-ASIN defense, auto close/loose/substitute/complement, launch/rank-defense, and exploratory discovery where data supports it.
- Existing exact keywords, negatives, product targets, and campaign routing rules when available.
- Destination delivery feasibility: destination campaign/ad group state, budget status, negative conflicts, advertised ASIN fit, and whether the destination can receive traffic.

## Missing Data Handling

- Missing margin or target ACoS/CPA: avoid firm profitability claims; use ACoS/ROAS/CPA only as proxies.
- Missing search term source mapping: do not recommend source negatives or precise routing.
- Missing destination campaign structure: propose a destination pattern, but mark the action `Needs Destination`.
- Missing existing exact keywords/targets: flag duplicate-risk before launching new exact terms.
- Missing current negative map: do not mark harvest or destination rows `APPROVAL_READY`.
- Missing exact profile, campaign, ad group, keyword, target, or destination IDs: keep write rows below `APPROVAL_READY`.
- Missing purchased-product data: avoid ASIN leakage conclusions.
- Missing inventory or Featured Offer / Buy Box: do not recommend aggressive bid or budget scale.
- Missing comparison period: classify by current signal strength and confidence, not trend.

## Write-Readiness Statuses

Every action row must use exactly one status:

- `PLANNING_ONLY`: strategic recommendation, destination pattern, or analysis that is not a live write candidate.
- `NEEDS_DATA`: required report, exact ID, destination, product context, economics, duplicate check, negative check, or strategic role is missing.
- `BLOCKED`: unsafe or non-executable due to duplicate conflict, negative conflict, broad negative blast radius, brand/own-ASIN/launch/rank protection, retail-readiness blocker, budget-starved destination, mixed ad-type contamination, or failed gate.
- `APPROVAL_REQUIRED`: row is specific enough to review, but still needs explicit human approval and live preflight before any write.
- `APPROVAL_READY`: human can approve the exact row after verifying live preflight. This status is rare and requires all readiness fields below.

No row may be `APPROVAL_READY` unless it includes exact profile/account, marketplace, ad type, source campaign ID, source ad group ID, destination campaign ID, destination ad group ID, keyword/target or negative ID where applicable, normalized search term, match type, current state, current value, proposed value, proposed action, duplicate checks, current negative checks, destination feasibility, approval text, preflight checks, readback checks, and 3/7/14-day monitoring criteria.

## Hard Blockers

Classify the row as `BLOCKED` or `NEEDS_DATA`, not `APPROVAL_READY`, when any of these apply:

- Existing exact keyword or product target already covers the normalized term, unless the action is delivery repair for an existing entity.
- Existing exact exists but is paused, archived, budget-starved, blocked by a negative, or in the wrong destination; classify as `Scale Existing Exact / Delivery Fix`, not duplicate harvest.
- Existing keyword/target report is missing; classify harvest rows as `NEEDS_DATA`.
- Current negative map is missing or destination has a negative that would block delivery.
- Destination campaign/ad group is missing, paused, budget-starved, wrong ASIN, wrong traffic type, or missing exact IDs.
- Search term is a brand-defense, own-ASIN-defense, launch/rank, or strategic discovery term and the proposed source negative would cut protected traffic.
- Competitor conquesting term has high ACoS but the source campaign's strategic role is conquesting or share defense; prefer `Bid Down / Keep Learning`, `Watchlist`, or controlled test.
- One order, one large order, or thin samples create attractive ACoS; use `Controlled Test` or `Watchlist`, not `Harvest Ready`.
- Negative phrase would block relevant query families, own-brand variants, size/color variants, or profitable discovery. Use narrower negative exact or block the negative.
- Sponsored Products, Sponsored Brands, and Sponsored Display data are blended and cannot be separated for the action.
- Product readiness, inventory, Featured Offer / Buy Box, margin, or listing relevance could change the decision and is unavailable.

## Evidence Thresholds

Use user-provided thresholds when available. Otherwise use these defaults, adjusted for product price, category, lifecycle stage, and account volume:

- `Harvest Ready`: at least 2-3 orders, relevant intent, ACoS/CPA within target economics, acceptable CVR, no retail-readiness blocker, duplicate checks passed, current negative checks passed, destination is feasible, and a clear exact destination exists.
- `Controlled Test`: 1-2 orders or promising CVR/CTR but not enough volume for a confident harvest; use lower bid, limited budget, or watchlist.
- `Scale Existing Exact`: the term already exists as exact and has enough profitable volume; recommend delivery, bid, budget, state, negative-conflict, or placement review instead of duplicate harvesting.
- `Product Target Candidate`: search term or purchased ASIN indicates an ASIN target should be tested, with relevance and economics checked.
- `Bid Down / Keep Learning`: relevant term with orders but above target economics; reduce bid only when current evidence and strategic role support it.
- `Negative Candidate`: irrelevant or structurally mismatched term, or spend exceeds 1.5-2.0x target CPA with zero orders and no strategic defense, launch, ranking, or discovery reason.
- `Watchlist`: below threshold, missing data, unclear relevance, or strategic role not yet resolved.

Do not overfit tiny samples. If evidence is thin, use `Watchlist`, `Controlled Test`, or `Needs Data`.

Lifecycle adjustments:

- Launch/rank window: tolerate higher ACoS only when the rank objective, budget cap, stop-loss, inventory, and monitoring rules are explicit.
- Brand defense: prioritize coverage and defensive routing over short-window ACoS, but do not add source negatives without approved defense coverage.
- Mature profit campaign: require economics, duplicate checks, and stable CVR before harvesting or bid increases.
- Exploration/discovery: prefer controlled tests and watchlists over negatives until waste is isolated.

## Traffic-Type Routing Matrix

| Traffic Type | Preferred Destination | Source Negative Default | Key Gate |
|---|---|---|---|
| Brand defense | Brand exact or defense ad group | Blocked unless defense coverage is approved and verified | Preserve branded and own-brand demand. |
| Category generic | Nonbrand exact by ASIN/product group | Negative exact only after destination delivery is verified | Check relevance, margin, inventory, and duplicate exacts. |
| Competitor brand | Competitor/conquest exact campaign | Usually blocked; bid down or controlled test first | Confirm strategic role and expected ACoS tolerance. |
| Own-ASIN defense | Own-ASIN product-target or defense campaign | Blocked unless own-ASIN defense is intentionally rerouted | Requires ASIN map and purchased-product context. |
| Substitute/complement ASIN | Product-target test | Blocked until ASIN relationship is known | Avoid own-ASIN or irrelevant target mistakes. |
| Launch/rank | Rank-support exact or launch campaign | Blocked unless launch/rank coverage is preserved | Requires objective, stop-loss, inventory, and monitoring. |
| Discovery/exploratory | Controlled exact test or watchlist | Blocked unless waste is isolated | Do not cut learning from thin samples. |
| Irrelevant query family | No destination, negative review | Negative exact or narrow phrase only | Phrase negatives need blast-radius proof. |

## Harvest Safety Gates

Before recommending an exact harvest, check:

- Normalize the search term for case, punctuation, plural/singular variants, spacing, ASIN casing, and simple token order differences before duplicate checks.
- The search term is not already isolated as an exact keyword or product target unless the action is to fix routing, state, delivery, budget, or negative conflicts.
- The destination campaign/ad group is known or the output clearly proposes one.
- The destination matches traffic type and business goal: branded, category generic, competitor, own-ASIN defense, rank-growth, profit, discovery, or product targeting.
- Destination delivery is feasible: enabled state, budget headroom or budget plan, no current negative conflict, correct advertised ASIN/product group, and exact destination IDs when claiming approval readiness.
- The advertised ASIN is retail-ready enough for the traffic.
- The term is relevant to the destination ASIN or product group.
- The proposed match type, bid direction, budget stance, and negative strategy are explicit.

Before recommending a source negative, check:

- The term has been safely captured elsewhere or the source traffic is clearly wasteful.
- Adding a negative will not cut brand defense, own-ASIN defense, launch/rank-defense, or profitable discovery.
- The negative scope is correct: campaign-level versus ad-group-level.
- The negative match type is justified: negative exact for routing control, negative phrase only for clearly irrelevant query families.
- Blast radius is reviewed: blocked tokens, variants, brand terms, ASINs, size/color variants, and profitable nearby queries are not harmed.

## Machine-Readable Action Row Schema

When producing action rows, include this schema in table form or JSON-like rows:

```text
row_id
action_type
write_readiness
profile_or_account
marketplace
ad_type
source_campaign_id
source_campaign_name
source_ad_group_id
source_ad_group_name
search_term_normalized
traffic_type
classification
destination_campaign_id
destination_campaign_name
destination_ad_group_id
destination_ad_group_name
keyword_or_target_id
negative_entity_id
match_type
current_state
current_value
proposed_value
proposed_action
source_negative_decision
duplicate_check
current_negative_check
destination_feasibility
product_readiness
reason
primary_risk
confidence
approval_text
preflight_checks
readback_checks
monitoring_3d
monitoring_7d
monitoring_14d
```

Use `missing` for unavailable IDs or checks; do not invent them. If any required field for a live write is `missing`, the row cannot be `APPROVAL_READY`.

## Workflow

1. Establish data coverage and freshness.
   - State windows, ad types, report freshness, attribution caveats, search-term grain, missing source/destination fields, and duplicate-risk.

2. Segment search terms.
   - Classify terms by traffic type, source campaign/ad group, advertised ASIN, purchased ASIN where available, and strategic role.

3. Score harvest candidates.
   - Evaluate orders, spend, sales, ACoS/CPA, ROAS, CVR, CPC, relevance, margin fit, retail readiness, lifecycle stage, destination clarity, duplicate risk, current negative conflicts, source-negative blast radius, and incrementality caveats.

4. Decide the route.
   - Assign each meaningful term to one primary outcome: `Harvest Ready`, `Controlled Test`, `Scale Existing Exact`, `Product Target Candidate`, `Bid Down / Keep Learning`, `Negative Candidate`, `Watchlist`, or `Needs Data`.

5. Build action rows.
   - Use the machine-readable schema and write-readiness statuses.
   - No row can be `APPROVAL_READY` unless all required exact IDs, current/proposed values, duplicate checks, negative checks, destination feasibility, approval text, preflight, readback, and monitoring fields are complete.

6. Define monitoring.
   - 3-day pass: destination entity is enabled, receives impressions/clicks, and is not blocked by negatives, state, or budget.
   - 7-day pass: spend, clicks, orders, CPC, and CVR are within expected range; source traffic did not collapse unexpectedly.
   - 14-day pass: ACoS/CPA, ROAS, route quality, duplicate traffic, and query drift are acceptable.
   - Failure criteria should name the rollback, bid-down, negative-review, or watchlist response.

## Output Format

Return these sections unless the user asks for a shorter version:

1. **Data Coverage And Harvest Gate**: windows, sources, missing fields, duplicate-risk, destination clarity, retail-readiness caveats, and whether harvest actions are action-safe.
2. **Executive Summary**: top harvest-ready terms, blocked terms, negative-risk warnings, and budget/bid posture.
3. **Search Term Classification Table**: Search Term | Source Campaign / Ad Group | Traffic Type | Orders | Spend | Sales | ACoS/CPA | Relevance | Destination | Classification | Confidence.
4. **Harvest Action Rows**: include the machine-readable schema fields, especially write readiness, exact IDs, current/proposed values, duplicate check, current negative check, destination feasibility, approval text, preflight, readback, and monitoring fields.
5. **Negative And Routing Decisions**: explain which source negatives are safe, blocked, or need more data.
6. **Blocked / Watchlist Terms**: terms below threshold, missing data, duplicate-risk, retail-readiness blocked, or strategically sensitive.
7. **Monitoring Plan**: 3-day, 7-day, and 14-day checks with success/failure criteria.
8. **Missing Data / Next Pulls**: existing exact keywords, negatives, target report, purchased-product report, margin, inventory, Featured Offer / Buy Box, and destination structure.

## Live Execution

This skill proposes actions only. If connected to Rocketcart MCP or another live execution layer, do not create keywords, negatives, targets, bid changes, budgets, or campaigns without explicit approval, live preflight, exact entity IDs, current/proposed values, readback, and monitoring criteria.

## Future Rocketcart-Aware Responsibilities

Keep this skill standalone for now. If a future Rocketcart-aware workflow uses these rows:

- Resolver: map profile, campaign, ad group, keyword, target, negative, product-ad, ASIN, and destination names to exact live IDs.
- Preflight: verify duplicate exacts/targets, current negatives, destination state, budget feasibility, current bids/states, product readiness, and source-negative blast radius immediately before approval or execution.
- Approval queue: show only exact rows with current/proposed values, reason, risk, confidence, approval text, preflight, readback, and monitoring fields.
- Execution: execute only explicitly approved rows after preflight; never execute planning rows, rows with missing IDs, or rows whose current state changed.
- Readback and monitoring: confirm created/changed entities, delivery, source traffic health, and 3/7/14-day performance outcomes.
