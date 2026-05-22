---
name: amazon-search-term-harvest-planner
description: Find Amazon Ads search terms ready for exact-match harvesting from auto, broad, phrase, or other discovery campaigns. Use when Codex needs to classify search terms by harvest readiness, choose safe destination campaigns/ad groups, decide whether source negatives are justified, and produce approval-gated Sponsored Products or Sponsored Brands action rows without unsafe negatives, duplicate routing, brand-defense cuts, or low-sample overfitting.
---

# Amazon Search Term Harvest Planner

## Purpose

Turn Amazon Ads search term data into a safe, specific harvesting plan. Identify search terms that deserve exact-match isolation, product-target expansion, bid direction, destination routing, or watchlist treatment. Do not treat every converting query as harvest-ready, and do not add source negatives unless routing or waste evidence supports it.

Optimize for clean traffic control, profitable growth, and learning. Preserve brand defense, own-ASIN defense, launch/rank-defense traffic, and strategically valuable discovery until the data proves a safer route.

## Required Inputs

Gather, derive, or mark unavailable:

- Marketplace, profile/account, currency, timezone, ad type, and date windows.
- Search term report with campaign, ad group, search term, match type/source targeting where available, impressions, clicks, spend, orders, sales, ACoS/ROAS, CPC, CTR, and CVR.
- Targeting or keyword report with existing keywords/targets, match type, bids, states, and campaign/ad group destinations.
- Campaign and ad group structure: targeting type, naming, budgets, states, portfolio, advertised ASINs, and strategic role.
- Product context: advertised ASIN, purchased ASIN where available, parent/child relationship, category, price, margin or target ACoS/CPA, inventory, Featured Offer / Buy Box, reviews, rating, delivery promise, and listing readiness.
- Traffic segmentation: branded, own-brand generic, category generic, competitor brand, competitor ASIN, own-ASIN defense, auto close/loose/substitute/complement, launch/rank-defense, and exploratory discovery where data supports it.
- Existing exact keywords, negatives, product targets, and campaign routing rules when available.

## Missing Data Handling

- Missing margin or target ACoS/CPA: avoid firm profitability claims; use ACoS/ROAS/CPA only as proxies.
- Missing search term source mapping: do not recommend source negatives or precise routing.
- Missing destination campaign structure: propose a destination pattern, but mark the action `Needs Destination`.
- Missing existing exact keywords/targets: flag duplicate-risk before launching new exact terms.
- Missing purchased-product data: avoid ASIN leakage conclusions.
- Missing inventory or Featured Offer / Buy Box: do not recommend aggressive bid or budget scale.
- Missing comparison period: classify by current signal strength and confidence, not trend.

## Evidence Thresholds

Use user-provided thresholds when available. Otherwise use these defaults, adjusted for product price, category, lifecycle stage, and account volume:

- `Harvest Ready`: at least 2-3 orders, relevant intent, ACoS/CPA within target economics, acceptable CVR, no retail-readiness blocker, and a clear exact destination.
- `Controlled Test`: 1-2 orders or promising CVR/CTR but not enough volume for a confident harvest; use lower bid, limited budget, or watchlist.
- `Scale Existing Exact`: the term already exists as exact and has enough profitable volume; recommend bid, budget, or placement review instead of duplicate harvesting.
- `Product Target Candidate`: search term or purchased ASIN indicates an ASIN target should be tested, with relevance and economics checked.
- `Bid Down / Keep Learning`: relevant term with orders but above target economics; reduce bid only when current evidence and strategic role support it.
- `Negative Candidate`: irrelevant or structurally mismatched term, or spend exceeds 1.5-2.0x target CPA with zero orders and no strategic defense, launch, ranking, or discovery reason.
- `Watchlist`: below threshold, missing data, unclear relevance, or strategic role not yet resolved.

Do not overfit tiny samples. If evidence is thin, use `Watchlist`, `Controlled Test`, or `Needs Data`.

## Harvest Safety Gates

Before recommending an exact harvest, check:

- The search term is not already isolated as an exact keyword or product target unless the action is to fix routing.
- The destination campaign/ad group is known or the output clearly proposes one.
- The destination matches traffic type and business goal: branded, category generic, competitor, own-ASIN defense, rank-growth, profit, discovery, or product targeting.
- The advertised ASIN is retail-ready enough for the traffic.
- The term is relevant to the destination ASIN or product group.
- The proposed match type, bid direction, budget stance, and negative strategy are explicit.

Before recommending a source negative, check:

- The term has been safely captured elsewhere or the source traffic is clearly wasteful.
- Adding a negative will not cut brand defense, own-ASIN defense, launch/rank-defense, or profitable discovery.
- The negative scope is correct: campaign-level versus ad-group-level.
- The negative match type is justified: negative exact for routing control, negative phrase only for clearly irrelevant query families.

## Workflow

1. Establish data coverage and freshness.
   - State windows, ad types, report freshness, attribution caveats, search-term grain, missing source/destination fields, and duplicate-risk.

2. Segment search terms.
   - Classify terms by traffic type, source campaign/ad group, advertised ASIN, purchased ASIN where available, and strategic role.

3. Score harvest candidates.
   - Evaluate orders, spend, sales, ACoS/CPA, ROAS, CVR, CPC, relevance, margin fit, retail readiness, destination clarity, duplicate risk, and incrementality caveats.

4. Decide the route.
   - Assign each meaningful term to one primary outcome: `Harvest Ready`, `Controlled Test`, `Scale Existing Exact`, `Product Target Candidate`, `Bid Down / Keep Learning`, `Negative Candidate`, `Watchlist`, or `Needs Data`.

5. Build action rows.
   - Include source campaign/ad group, search term, destination campaign/ad group, match type, suggested bid direction, source negative decision, reason, risk, confidence, and approval status.

6. Define monitoring.
   - For harvested terms, define 3-day delivery checks, 7-day spend/order checks, and 14-day ACoS/CVR/route-quality checks.

## Output Format

Return these sections unless the user asks for a shorter version:

1. **Data Coverage And Harvest Gate**: windows, sources, missing fields, duplicate-risk, destination clarity, retail-readiness caveats, and whether harvest actions are action-safe.
2. **Executive Summary**: top harvest-ready terms, blocked terms, negative-risk warnings, and budget/bid posture.
3. **Search Term Classification Table**: Search Term | Source Campaign / Ad Group | Traffic Type | Orders | Spend | Sales | ACoS/CPA | Relevance | Destination | Classification | Confidence.
4. **Harvest Action Rows**: Source Campaign | Source Ad Group | Search Term | Destination Campaign / Ad Group | Match Type | Bid Direction | Source Negative? | Reason | Risk | Confidence | Approval.
5. **Negative And Routing Decisions**: explain which source negatives are safe, blocked, or need more data.
6. **Blocked / Watchlist Terms**: terms below threshold, missing data, duplicate-risk, retail-readiness blocked, or strategically sensitive.
7. **Monitoring Plan**: 3-day, 7-day, and 14-day checks with success/failure criteria.
8. **Missing Data / Next Pulls**: existing exact keywords, negatives, target report, purchased-product report, margin, inventory, Featured Offer / Buy Box, and destination structure.

## Live Execution

This skill proposes actions only. If connected to Rocketcart MCP or another live execution layer, do not create keywords, negatives, targets, bid changes, or campaigns without explicit approval, live preflight, exact entity IDs, readback, and monitoring criteria.
