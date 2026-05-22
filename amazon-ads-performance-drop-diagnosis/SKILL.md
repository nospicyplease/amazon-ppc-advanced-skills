---
name: amazon-ads-performance-drop-diagnosis
description: Diagnose why Amazon advertising performance declined for a product, ASIN, campaign, marketplace, or account. Use when the user asks why sales, orders, ROAS, ACOS, TACoS, profit, BSR, rank, traffic, conversion rate, or campaign performance dropped, and needs Amazon Ads data connected with BSR/rank, competitor movement, retail readiness, attribution scope, campaign history, and action-safe recovery recommendations.
---

# Amazon Ads Performance Drop Diagnosis

## Objective

Diagnose the cause of a decline. Do not produce a generic performance recap. Trace when the break started, quantify the impact, isolate the entities causing the loss, connect ads movement to BSR/rank movement, and recommend only the actions supported by evidence gates. Protect sales velocity and organic momentum; do not optimize only for lower ACOS or lower spend.

## Required Inputs

Gather, derive from available data, or mark unavailable before diagnosing:

- Marketplace, profile/account, currency, timezone, and ASIN/product/campaign scope.
- Suspected drop window and baseline comparison period.
- Primary KPI and target KPI, such as sales, orders, ACOS, TACoS, ROAS, BSR, profit, or rank.
- Amazon Ads metrics by SP/SB/SD where available: spend, sales, orders, impressions, clicks, CTR, CPC, CVR, ACOS, ROAS, budgets, budget usage, placements, campaigns, ad groups, keywords, targets, search terms, product ads, advertised ASINs, and purchased ASINs.
- Total retail sales/orders for TACoS or organic-momentum claims; if unavailable, do not diagnose TACoS.
- BSR/rank history for the affected advertised ASINs, including category and date granularity.
- Retail readiness: Buy Box, stock, suppression, Prime/FBA/shipping promise, price, coupon/promo/deal, reviews/ratings, listing/content changes, and parent/child variation changes.
- Change history: bids, budgets, placements, states, product ads, negatives, campaign launches, pauses, portfolio budgets, budget rules, automated rules, bulk edits, and third-party optimization changes.
- Competitor/category context: competitor BSR/rank, price, coupon/deal, reviews/ratings, stock, ad visibility, and category demand where available.

## Diagnostic Gates

Start every diagnosis with a data reliability and actionability gate:

- Classify the case as `Actionable`, `Directional`, or `Non-actionable`.
- Print exact windows, freshness/T-1 status, ad type scope, attribution window, ASIN scope, and any reconciliation gaps.
- Flag mixed-ASIN contamination, brand-halo/view-through risk, reporting lag, missing BSR, missing total sales, missing retail readiness, missing competitor data, or weak sample size.
- Do not make definitive root-cause claims when missing data could materially change the diagnosis.
- Do not recommend bid, budget, negative, pause, or relaunch execution unless the relevant action gate in the diagnostic reference is satisfied.

## Workflow

1. Establish data coverage, freshness, and exact windows.
   - Anchor recent windows on T-1 when current data may be incomplete.
   - Print exact date ranges used for L7, L14, L30, L60, L90, suspected drop, and baseline.
   - Separate SP, SB, and SD when the data supports it; do not blend ad types unless the user asks for an all-ad-type view.
   - Normalize uneven windows to per-day values before comparing them.

2. Find the break point.
   - Inspect daily or weekly trends for the first sustained change in sales/orders, clicks, impressions, CPC, CVR, ACOS/ROAS, TACoS, budget usage, placement mix, and BSR.
   - Build a control-change timeline for at least 14 days before the break through the drop window.
   - For each suspected break date, list budget, bid, placement, state, product ad, portfolio, budget rule, automation, negative, or structure changes within +/- 7 days.
   - Mark whether the break is abrupt, gradual, intermittent, or isolated to a campaign/entity.

3. Quantify impact and decompose drivers.
   - Build an impact table with baseline, drop window, absolute delta, percent delta, per-day delta, confidence, and driver read.
   - Use bridge math where possible: traffic effect, conversion effect, ASP/AOV effect, CPC/spend effect, mix effect, and control-change effect.
   - Include spend efficiency and volume together. ACOS, ROAS, and TACoS changes are symptoms; do not treat them as root causes.

4. Isolate the biggest contributors.
   - Rank campaigns, ad groups, keywords, targets, search terms, product ads, advertised ASINs, and purchased ASINs by lost sales/day, lost orders/day, wasted spend, share of total delta, BSR sensitivity, previous-winner status, current state, and attribution risk.
   - Segment query mix into branded defense, own-ASIN defense, category generic, competitor brand, competitor ASIN, auto close/loose/substitute/complement, launch/rank-defense, and exploratory discovery where data supports it.
   - Decompose placements for Top of Search, Rest of Search, and Product Pages when placement data exists.

5. Connect PPC, retail readiness, competitors, and BSR.
   - Compare timing and direction of ad orders, total orders, organic sales proxy, retail-readiness changes, BSR/rank, category demand, and competitor rank/offer movement.
   - Decide whether PPC decline likely caused rank deterioration, rank deterioration likely weakened PPC, both reinforced each other, or both were driven by retail, competitor, or market movement.
   - Treat BSR as a velocity signal, not a standalone cause. Explain the mechanism and confidence.

6. Recommend recovery actions only after gates.
   - Prioritize restoring qualified traffic, conversion, and rank defense before cosmetic ACOS cuts.
   - Avoid spend cuts when spend defends rank, launch velocity, brand defense, or organic momentum unless waste is clearly isolated and low-risk.
   - Separate facts, likely causes, assumptions, missing data, and watchlist items.
   - Keep write actions approval-gated when the environment supports live mutation.

## Output Format

Always return these sections, in this order:

1. **Data Reliability And Actionability Gate**: available data, missing data, reconciliation issues, attribution/scope risks, sample-size confidence, and whether bid/budget/negative/pause/relaunch recommendations are action-safe.
2. **Executive Verdict**: 3-6 bullets with the most likely cause, confidence, impact, what to do first, and which major causes cannot be ruled out because of missing data.
3. **Drop Timeline**: exact dates, break point, control changes, and whether ads, retail readiness, competitors, or BSR moved first.
4. **Impact Summary Table**: baseline vs drop window with deltas, per-day values, confidence, and driver read for the primary KPI and driver metrics.
5. **Root-Cause Diagnosis**: facts, likely causes, assumptions, and missing/unreliable data.
6. **Biggest Losers**: campaigns, ad groups, keywords, targets, search terms, product ads, advertised ASINs, and purchased ASINs ranked by business impact and attribution risk.
7. **BSR And Competitor Interpretation**: whether PPC hurt rank, rank hurt PPC, both reinforced each other, or retail/competitor/market factors drove both.
8. **Recommended Actions**: prioritized by expected impact, confidence, urgency, reversibility, rank/velocity risk, and action-gate status.
9. **Verification Plan**: what to check after 3, 7, and 14 days, including KPI thresholds and rollback/scale criteria.

## Diagnostic Reference

Always read [drop-diagnosis-framework.md](references/drop-diagnosis-framework.md) before completing a diagnosis. Use it for cause signatures, decomposition formulas, output table templates, confidence rules, action gates, BSR interpretation, TACoS validation, retail readiness, competitor movement, budget and placement diagnosis, mixed-ASIN contamination, and recommendation safety.
