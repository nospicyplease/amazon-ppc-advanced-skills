# Drop Diagnosis Framework

Use this reference to turn Amazon Ads and BSR data into a causal diagnosis with recommendation safety gates.

## Contents

- Window Design
- Data Reliability And Actionability Gate
- ASIN Action-Safety Gate
- Statistical Confidence And Materiality
- Core Decomposition
- TACoS Rules
- Retail Readiness Gate
- Budget And Pacing Diagnosis
- Placement Mix Diagnosis
- Cause Signatures
- Campaign History Diagnosis
- Negative Change Relevance
- BSR Causality Tests
- Biggest-Loser Ranking
- Action Gates
- Output Table Templates
- Recommended Action Prioritization
- Verification Plan

## Window Design

Use these windows unless the user specifies another structure:

- L7 and L14 for the current tactical break.
- L30 for recent baseline and volatility control.
- L60 and L90 for structural context, seasonality, and pre-drop winners.
- User-provided suspected drop and baseline windows when they are more specific than rolling windows.

Compare per-day metrics when windows have different lengths. For very low-volume products, prefer L14/L30/L60 over L7 and state that confidence is limited by sample size.

## Data Reliability And Actionability Gate

Before diagnosing root cause, classify the case as one of:

- `Actionable`: required data is available, date-aligned, reconciled enough for the decision, and sample size supports the conclusion.
- `Directional`: enough data exists to identify likely drivers, but missing data or sample size limits confidence. Recommendations must be conservative and verification-led.
- `Non-actionable`: missing or conflicting data could materially change the diagnosis. Provide likely hypotheses and the exact data needed before bid, budget, pause, negative, or relaunch decisions.

Check and report:

- Date range, timezone, marketplace, currency, profile/account, and ASIN scope.
- Ad type scope: SP, SB, SD, or blended.
- Attribution window and reporting freshness.
- Whether sales are ad-attributed sales, total retail sales, advertised-ASIN sales, purchased-ASIN sales, brand-halo sales, or view-through sales.
- Whether campaign, search-term, advertised-product, purchased-product, BSR, and total retail sales reconcile directionally.
- Whether campaigns/ad groups include multiple advertised ASINs.
- Whether BSR/rank data uses the same ASIN, category, date granularity, and parent/child or variation context.
- Whether retail intelligence data has freshness and coverage labels, and whether each claim is based on dated history or a point-in-time snapshot.
- Whether competitor/category data is available; if not, external share shift cannot be ruled out.
- Whether observed changes happened before/during the drop window or only after the drop as a fix.

## ASIN Action-Safety Gate

For ASIN-scoped diagnoses, separate diagnosis confidence from execution safety.

Check and report:

- Whether product-level KPIs for the advertised ASIN reconcile and have complete-enough daily coverage.
- Whether keyword, target, search-term, and placement rows are cleanly scoped to the affected ASIN or pass through mixed-ASIN campaigns/ad groups.
- Whether advertised-ASIN sales, purchased-ASIN sales, same-SKU sales, other-SKU halo, brand-halo, or view-through sales materially change interpretation.
- Whether search-term sales can be attributed to the affected ASIN, or only to a mixed ad group/campaign.
- Whether the affected ASIN also appears in untouched campaigns that confirm or contradict the same drop pattern.

Classify action safety:

- `Action-safe`: Product-level KPIs are reliable, entity-level rows are ASIN-clean or otherwise reconciled, sample size is sufficient, and retail readiness risk is not the primary unresolved driver.
- `Directional only`: Product-level diagnosis is useful, but keyword/target/search-term actions require caution because of mixed scope, weak sample size, missing retail data, or partial reconciliation.
- `Blocked`: Entity-level writes such as bid cuts, negatives, pauses, or relaunches could harm the wrong ASIN or suppress previously valuable demand. Recommend isolation, manual review, or more data first.

Do not let a clean ASIN-level product drop automatically authorize keyword, target, negative, or pause actions when those entities are contaminated by mixed-ASIN scope.

## Statistical Confidence And Materiality

Do not treat every delta as causal. Classify each major finding as high, medium, or low confidence.

Use high confidence only when:

- The break is visible across aligned daily/weekly data.
- The affected entity has enough volume to support the claim.
- The same driver appears in multiple related metrics, such as clicks down before orders down, or CVR down while clicks remain stable.
- Known changes or external events align with the break.

Use medium confidence when directional evidence is clear but one major data source is missing, sample size is moderate, or timing aligns but magnitude is partially uncertain.

Use low confidence when click/order volume is low, the drop window is short, attribution/ASIN scope is unclear, retail readiness is missing, or competitor/category data is missing and external share shift is plausible.

Practical sample-size rules:

- Do not call a search-term CVR decline material from fewer than 100 clicks unless spend or order loss is business-critical.
- Do not call a keyword/target winner or loser from fewer than 3 orders unless supported by longer history.
- Treat CTR changes as weak evidence unless impressions are large enough to make the movement stable.
- For zero-order waste, compare spend to target CPA, margin, or historical conversion rate before recommending negatives or pauses.
- For low-volume ASINs, prefer L14/L30/L60 over L7 and state confidence limits.

## Core Decomposition

Use these relationships to identify the driver rather than repeating the symptom:

- Ad sales roughly move with clicks x CVR x average selling price.
- Clicks move with impressions x CTR.
- Spend moves with clicks x CPC.
- ACOS worsens when spend rises faster than sales or sales falls faster than spend.
- TACoS worsens when ad spend grows without total sales support, or total sales falls while ads keep defending volume.
- BSR usually worsens when total sales velocity falls relative to category competitors.

Use bridge math whenever enough baseline and drop-window data exists. Include impressions, clicks, CTR, CPC, spend, orders, CVR, AOV/ASP, sales, ACOS, and ROAS:

1. Baseline clicks x baseline CVR x baseline ASP = baseline modeled sales.
2. Drop clicks x baseline CVR x baseline ASP = traffic effect.
3. Drop clicks x drop CVR x baseline ASP = conversion effect.
4. Drop clicks x drop CVR x drop ASP = ASP/AOV effect.
5. Reconcile modeled delta to actual sales/orders delta and label unexplained mix, attribution, or data gaps.

Classify the primary driver as one of:

- Traffic loss.
- CPC inflation.
- Conversion-rate decline.
- AOV/ASP decline.
- Query or placement mix shift.
- Control-change driven.
- Retail-readiness driven.
- BSR/rank driven.
- Market or competitor driven.
- Mixed or unresolved.

Report driver deltas in this order:

1. Sales/orders delta.
2. Traffic delta: impressions, clicks, CTR.
3. Cost delta: CPC and spend per click/order.
4. Conversion delta: CVR, orders per click, retail/listing/offer factors.
5. Mix delta: search terms, targets, match types, placements, branded/non-branded, ASIN traffic.
6. Control delta: budgets, bid changes, state changes, placement modifiers, campaign launches/pauses.
7. Rank delta: BSR and competitor rank timing.

## TACoS Rules

Only diagnose TACoS when total retail sales/orders are available for the same ASIN or product group, marketplace, date range, and currency.

If total retail sales are unavailable:

- Do not calculate TACoS.
- Do not infer organic sales movement from ad-attributed sales alone.
- Use ACOS/ROAS and ad sales/orders only.
- State that PPC-to-organic and PPC-to-BSR causality is provisional.

Read TACoS movement by combining ad spend change, total sales/orders change, ad sales/orders change, BSR/rank movement, and organic sales proxy when available. A worsening TACoS is not automatically bad if spend is intentionally defending rank, launch velocity, or high-value organic terms. A better TACoS is not automatically good if sales velocity and BSR deteriorated.

## Retail Readiness Gate

Before recommending PPC bid or budget cuts for a broad CVR or sales decline, check whether the affected ASIN had:

- Buy Box loss or instability.
- Out-of-stock, low stock, suppressed listing, or delivery promise degradation.
- Prime/FBA status change.
- Price increase or loss of price competitiveness.
- Coupon, promo, deal, Subscribe & Save, or merchandising change.
- Review rating decline or review-count disadvantage.
- Main image, title, bullet, A+ content, variation, parent/child, or catalog change.
- Seller/account health or fulfillment issue.

Use retail intelligence data generically and require source freshness/coverage before interpreting trends. Distinguish:

- Dated history, which can support trend claims.
- Current offer snapshots, which can support current-state checks but cannot prove when a change happened.
- Missing or stale retail data, which should lower confidence and make recommendations verification-led.

If CVR falls across qualified traffic and retail readiness changed near the break, diagnose retail readiness before PPC structure. Do not recommend scaling traffic until retail blockers are resolved or explicitly ruled out.

## Budget And Pacing Diagnosis

Check whether sales/orders dropped because qualified traffic was budget-constrained.

Evidence:

- Budget usage increased to or near 100%.
- Campaigns went out of budget before the end of day.
- Strong campaigns were capped while weaker campaigns continued spending.
- Portfolio budgets, budget rules, account caps, billing issues, or dayparting constrained delivery.
- Daily budget cuts preceded impression/click/order loss.
- Impressions and clicks fell while CTR/CVR stayed stable or improved.

Likely actions:

- Restore or reallocate budget only to historically converting routes.
- Move budget from weak exploratory routes to proven high-intent campaigns.
- Avoid increasing budget when retail readiness is broken or query mix is poor.
- Monitor pacing at 3 days and 7 days after restoration.

## Placement Mix Diagnosis

For Sponsored Products and other reports where placement data is available, compare Top of Search, Rest of Search, and Product Pages by impressions/day, clicks/day, CPC, CTR, CVR, orders/day, sales/day, ACOS/ROAS, placement modifier, and share of total spend/sales.

Evidence of placement-driven decline:

- Top of Search clicks/orders fall before total sales falls.
- Product Pages or Rest of Search take a larger share of spend with lower CVR.
- Placement CPC rises materially while conversion does not support the higher cost.
- Placement modifier changes align with the break.
- A rank-sensitive term loses high-CVR Top of Search exposure.

Likely actions:

- Restore high-CVR placement exposure only where historical conversion and rank value support it.
- Reduce placement exposure where spend shifted into low-CVR traffic.
- Do not make account-wide bid cuts when the issue is placement mix.

## Cause Signatures

Use the strongest matching signature, and call out mixed causes when more than one is material.

### Traffic Loss

Evidence:

- Impressions and clicks fall before sales/orders fall.
- CTR may be stable, but reach disappears.
- Budget caps, bid cuts, lost placement exposure, paused entities, retail suppression, or eligibility issues may appear.

Likely actions:

- Restore bids/budgets only on historically converting campaigns or terms.
- Recover Top of Search or high-CVR placement exposure if it was the lost source.
- Re-enable or rebuild proven routes when a structure change removed traffic.

### CPC Increase

Evidence:

- CPC rises materially while clicks are flat/down and CVR is stable or only mildly down.
- Spend rises faster than orders.
- Competitor pressure or placement mix may shift toward expensive traffic.

Likely actions:

- Segment high-CPC terms by conversion and rank value.
- Lower or cap bids on non-strategic expensive traffic.
- Preserve bids on terms defending BSR or organic rank when conversion remains acceptable.

### Conversion-Rate Decline

Evidence:

- Clicks remain stable or rise, but orders and CVR fall.
- BSR may worsen after conversion loss, especially if total order velocity drops.
- Listing, price, coupon, stock, shipping, Buy Box, review, image, or competitor offer changes may explain the fall.

Likely actions:

- Fix offer/listing blockers before broad bid cuts.
- Shift traffic toward historically high-CVR queries and ASIN targets.
- Reduce exposure only on clearly unqualified traffic.

### Poor Query Mix

Evidence:

- Spend shifts toward lower-intent search terms, broad/auto waste, irrelevant ASINs, or generic expensive queries.
- Campaign totals worsen while some exact/product targets still work.
- CTR/CVR decline is concentrated in new or expanded traffic.

Segment query mix into:

- Branded defense.
- Own-ASIN/product defense.
- Category generic.
- Competitor brand.
- Competitor ASIN.
- Auto close match, loose match, substitutes, and complements.
- Launch or rank-defense terms.
- Exploratory discovery terms.

Compare each segment by sales/orders lost, spend retained, CVR, CPC, and rank/BSR sensitivity. Do not add negatives to strategic rank-defense, branded-defense, or own-ASIN-defense queries solely because short-term ACOS is high.

Likely actions:

- Harvest converting queries into controlled exact/product-target routes.
- Add negatives only where current waste evidence is clear.
- Trim or isolate exploratory routes without starving proven rank-defense terms.

### Negative Keyword Or Target Change

Evidence:

- A negative keyword or negative product target was added, removed, archived, or unarchived before or during the drop window.
- The changed negative was attached to the affected ASIN's serving campaign or ad group.
- The blocked or unblocked query/product target had meaningful historical sales, orders, rank value, or strategic value before the change.
- The affected ASIN did not drop in otherwise comparable campaigns that were untouched by the negative change.

Interpretation rules:

- Do not blame a negative change that happened only after the measured drop window; classify it as a post-drop fix or watch item.
- Do not blame a negative that belongs to a campaign/ad group that does not serve the affected ASIN.
- Do not assume semantic relevance is operational relevance. A query can sound related while living in a route that cannot affect the ASIN being diagnosed.
- When historical sales exist on the blocked/unblocked query or target, prefer restoration or isolation review over an immediate permanent negative.

Likely actions:

- Reverse or revise the specific harmful negative only when timing, attachment, historical sales, and unaffected-campaign checks support causality.
- Keep changes under watch when relevance is semantic but attachment or timing is weak.
- Use isolation or exact-route rebuilds when mixed-ASIN scope prevents safe negative decisions.

### Budget Or Bid Changes

Evidence:

- Break starts after budget reduction, bid drop, placement modifier change, campaign pause, rule/automation run, or out-of-budget increase.
- Traffic loss is concentrated in affected entities.

Likely actions:

- Reverse the specific damaging control change if performance history justifies it.
- Restore spend in stages with 3-day and 7-day monitoring.
- Avoid account-wide budget cuts if only a few routes caused waste.

### Campaign Structure Changes

Evidence:

- New campaigns, reused campaigns, ad group restructures, match-type shifts, changed product ad mapping, or disabled ads precede the drop.
- Learning/history reset or traffic rerouting changes query mix.

Likely actions:

- Compare old winners against new routes by query and ASIN.
- Relaunch with fresh history only when old routes are contaminated and the user explicitly wants new-history execution.
- Keep old winners live or phased down until new routes prove replacement volume.

### BSR Or Rank Decline

Evidence:

- BSR worsens before ad CTR/CVR/order decline.
- Competitors gain rank or category demand shifts before PPC weakens.
- PPC traffic still arrives but converts worse because rank/social proof/organic visibility deteriorated.

Interpretation rules:

- Lower BSR number means better rank; higher BSR number means worse rank.
- Compare BSR within the same category/subcategory and same child/parent context.
- BSR is not linear; small numeric changes near the top can be more meaningful than larger changes deeper in the category.
- Tie BSR to total order velocity, not ad sales alone.
- Allow for lag: ad traffic loss may hit BSR after a delay, and BSR decline may later weaken PPC CVR/CTR.

Likely actions:

- Defend high-intent rank terms and best ASIN targets instead of cutting all spend.
- Use focused promotions/coupons/price tests when offer weakness is likely.
- Rebuild sales velocity through terms with proven rank sensitivity.

### Competitor Movement

Evidence:

- Competitor BSR improves while own BSR and PPC CVR/CTR worsen.
- Competitor price, coupon, review count/rating, image/content, stock, or ad visibility improves near the break.

Compare against top organic competitors, top sponsored competitors, and direct substitute ASINs when available. Require date-aligned movement. If only a current competitor snapshot exists, label competitor conclusions low confidence.

Likely actions:

- Identify the competitor advantage and respond with offer, listing, or targeting changes.
- Avoid assuming campaign failure when market share shifted externally.

### Product, Listing, Or Offer Weakness

Evidence:

- CVR falls across otherwise qualified traffic.
- Organic and paid sales both weaken.
- Price increase, coupon removal, inventory issue, shipping promise degradation, Buy Box loss, review/rating drop, or listing change aligns with the break.

Likely actions:

- Fix offer/listing first.
- Use ads to route only the best demand while conversion recovers.
- Monitor BSR rebound and CVR before scaling spend.

### Seasonality Or Market Demand Shift

Evidence:

- Own traffic and competitor/category activity decline together.
- BSR movements are broad, not isolated.
- Search volume or category demand weakens without an account control change.

Likely actions:

- Reduce exploratory waste but keep efficient core demand capture.
- Compare to last year or prior seasonal windows when available.
- Shift budget to in-season products or terms.

### Data Attribution Or Multi-ASIN Contamination

Evidence:

- Campaign/ad group includes multiple advertised ASINs and metrics cannot be cleanly attributed.
- Sales totals do not reconcile across profile, campaign, ASIN, and search-term levels.
- Attribution windows, SP/SB/SD scope, brand halo sales, view-through sales, or reporting freshness differ between sources.

Before making ASIN-level conclusions, check:

- Number of advertised ASINs per campaign/ad group.
- Advertised ASIN vs purchased ASIN.
- Parent/child variation mapping.
- Brand halo sales, especially for Sponsored Brands.
- View-through or audience-driven sales, especially for Sponsored Display.
- Whether search-term sales can be tied to the affected ASIN.
- Whether total retail sales agrees directionally with ad-attributed sales.

If mixed-ASIN contamination is material, recommend at the cleanest reliable level. Do not pause, relaunch, or restructure ASIN-specific campaigns based only on contaminated aggregate campaign metrics.

## Campaign History Diagnosis

Build a control-change audit for at least 14 days before the break through the drop window. Also list post-drop fixes separately so they are not misclassified as causes. Track:

- Campaign/ad group/keyword/target/product ad state changes.
- Bid increases and bid decreases.
- Budget changes.
- Placement modifier changes.
- Match-type changes.
- New campaigns or ad groups.
- Newly enabled or removed keywords/targets.
- Paused or archived campaigns, ad groups, keywords, targets, or product ads.
- Negative keyword/target additions, removals, archives, and unarchives.
- Product ad mapping changes.
- Portfolio budget changes.
- Budget rules.
- Automated rules, bid automation, bulk uploads, or third-party tool changes.

Evidence:

- The break starts after a control change.
- Traffic loss is concentrated in changed entities.
- Query or placement mix changes after restructuring.
- Old winners lose delivery while new routes do not replace their order volume.

Likely actions:

- Reverse the specific harmful change where historical performance supports it.
- Restore old winners before scaling new replacements.
- Avoid relaunch unless old structure/history is materially contaminated.

## Negative Change Relevance

For every negative keyword or negative target that might explain a drop, answer four questions before assigning causality:

1. `Attachment`: Was the negative applied to a campaign/ad group that actually served the affected ASIN or entity?
2. `Timing`: Did the change happen before or during the measured drop window, not only after the drop as a fix?
3. `Historical value`: Did the blocked or unblocked query/product target have prior sales, orders, rank value, or strategic defense value?
4. `Untouched-route check`: Did the affected ASIN also drop in campaigns or ad groups that the negative could not affect?

If any answer is missing or weak, label the negative hypothesis `Directional` or `Rejected`, not causal. If mixed-ASIN scope prevents clean attribution, recommend ASIN isolation or manual review before writing new negatives.

## BSR Causality Tests

Use timing first, then magnitude:

- PPC likely caused BSR deterioration when ad orders/clicks fell first, total sales velocity fell next, and BSR worsened after that.
- BSR likely weakened PPC when BSR or competitor rank worsened first, then CTR/CVR fell while traffic availability remained similar.
- PPC and BSR likely reinforced each other when ad velocity loss and BSR decline occur within the same short window and both continue worsening.
- External market/competitor factors likely drove both when competitors or category demand moved first and own ads degrade after the market shift.

Before interpreting BSR/rank:

- Confirm retail intelligence freshness and rank-history coverage.
- Identify whether the data is dated history or a current snapshot.
- Handle multiple category or subcategory rank series explicitly; do not mix categories as one trend.
- Lower confidence when parent/child or variation-level rank sharing means the affected ASIN may not own the observed rank movement.

State confidence as high, medium, or low. Use low confidence when BSR data is sparse, only a snapshot is available, multiple category series conflict, competitor data is missing, volume is too low, or date alignment is weak.

## Biggest-Loser Ranking

Rank entities by business impact, not just spend:

- Lost sales dollars per day.
- Lost orders per day.
- Percent of total sales/order delta.
- Baseline share vs drop-window share.
- BSR-sensitive lost volume on core/high-rank terms.
- Wasted spend where spend remained high but orders disappeared.
- Strategic risk where a term or ASIN target previously drove rank or organic momentum.
- Previous winner flag.
- Current state, budget-capped, or placement-change flag.
- Mixed-ASIN or attribution-risk flag.

Do not bury a high-sales-loss entity below a high-ACOS but tiny-spend entity.

## Action Gates

Use these gates before recommending execution.

### Bid Increase Gate

Allowed only when lost traffic is on historically converting terms/targets, retail readiness is intact, CPC increase risk is acceptable, the term/target has rank/sales/conversion value, and budget is available or reallocated from weaker traffic.

### Bid Cut Gate

Allowed only when spend is material, inefficiency is sustained, the route is not defending rank/brand/launch velocity, ASIN/entity scope is action-safe, and retail readiness issues are not the primary cause.

### Budget Increase Gate

Allowed only when the campaign is capped or pacing-limited, historical conversion supports incremental spend, query/placement mix is qualified, and the ASIN is retail-ready.

### Budget Cut Gate

Allowed only when spend is funding material waste and lost sales/rank risk is low or covered by stronger routes. Do not starve proven high-intent or rank-sensitive terms.

### Negative Keyword/Target Gate

Allowed only when waste is current and material, click/spend volume is sufficient, ASIN/entity scope is action-safe, the query/target is not strategic/branded/own-ASIN/rank-sensitive, attachment and timing checks pass, historical-value checks do not show prior meaningful sales or defense value, untouched-route checks do not contradict causality, and there is no evidence that the issue is temporary retail readiness or stock-related.

### Pause Gate

Allowed only when the entity has sustained material waste or structural contamination, has no meaningful strategic value, ASIN/entity scope is action-safe, and safer alternatives such as bid reduction, isolation, or budget reallocation are insufficient.

### Relaunch Gate

Allowed only when structure, history, ASIN mapping, or query contamination materially impairs performance; old winning routes are preserved or phased down only after replacement volume proves out; and objective, success threshold, rollback rule, and rank-risk control are defined.

## Output Table Templates

Use compact tables. Add or remove columns only when the available data requires it.

### Data Reliability And Actionability Gate

| Area | Status | Evidence | Risk if missing | Actionability |
|---|---|---|---|---|
| Freshness/date range | | | | Actionable/Directional/Non-actionable |
| Ad type scope | | | | |
| Attribution/sales scope | | | | |
| ASIN mapping | | | | |
| Entity action safety | | | | Action-safe/Directional only/Blocked |
| Retail readiness | | | | |
| BSR/rank freshness and coverage | | | | |
| Competitor/category | | | | |
| Sample size | | | | |

### ASIN Action-Safety

| Area | Evidence | Risk | Status |
|---|---|---|---|
| Product-level KPI coverage | | | Reliable/Directional/Blocked |
| Mixed-ASIN campaign/ad group scope | | | Clean/Mixed/Unknown |
| Same-SKU vs other-SKU or halo attribution | | | Low/Material/Unknown |
| Search-term to affected-ASIN attribution | | | Clean/Directional/Blocked |
| Entity write safety | | | Action-safe/Directional only/Blocked |

### Impact Summary

| Metric | Baseline | Drop window | Abs delta | % delta | Confidence | Driver read |
|---|---:|---:|---:|---:|---|---|
| Sales/day | | | | | | |
| Orders/day | | | | | | |
| Spend/day | | | | | | |
| Impressions/day | | | | | | |
| Clicks/day | | | | | | |
| CTR | | | | | | |
| CPC | | | | | | |
| CVR | | | | | | |
| AOV/ASP | | | | | | |
| ACOS | | | | | | symptom only |
| ROAS | | | | | | symptom only |
| TACoS | | | | | | symptom only; only if total sales available |
| BSR/rank | | | | | | velocity signal |

### Control-Change Audit

| Change date | Timing vs drop | Entity level | Entity | Change type | Before | After | Historical performance | Attached to affected scope | Causal read |
|---|---|---|---|---|---|---|---|---|---|
| | Pre-drop/During-drop/Post-drop fix | Campaign/ad group/keyword/target/product ad/negative/placement/budget | | Bid/budget/state/placement/negative/new/removed | | | | Yes/No/Unknown | Cause/Watch/Rejected |

### Negative Change Relevance

| Negative | Scope | Timing | Attached to affected ASIN route | Historical sales/orders | Untouched-route check | Verdict |
|---|---|---|---|---|---|---|
| | Campaign/ad group | Pre-drop/During-drop/Post-drop fix | Yes/No/Unknown | Yes/No/Unknown | Confirms/Contradicts/Unknown | Causal/Directional/Rejected |

### Contribution Bridge

| Step | Modeled sales/orders | Delta vs prior step | Interpretation | Confidence |
|---|---:|---:|---|---|
| Baseline clicks x baseline CVR x baseline ASP | | | Baseline modeled demand | |
| Drop clicks x baseline CVR x baseline ASP | | | Traffic effect | |
| Drop clicks x drop CVR x baseline ASP | | | Conversion effect | |
| Drop clicks x drop CVR x drop ASP | | | ASP/AOV effect | |
| Actual drop-window result | | | Residual mix/attribution/data gap | |

### Biggest Losers

| Rank | Level | Entity | Baseline sales/day | Drop sales/day | Sales delta/day | % total delta | Orders delta/day | Previous winner | State/capped/change flag | Attribution risk | Driver | Action |
|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| 1 | Campaign/ad group/keyword/target/search term/product ad/ASIN | | | | | | | | | | | |

### Recommended Actions

| Priority | Action | Evidence | Gate status | Expected impact | Confidence | Urgency | Reversibility | Rank/velocity risk |
|---:|---|---|---|---|---|---|---|---|
| 1 | | | Passed/Blocked/Watch | high/medium/low | high/medium/low | immediate/this week/watch | easy/moderate/hard | protects rank/neutral/risks rank |

### Verification Plan

| Checkpoint | What to verify | Success threshold | Failure signal | Decision |
|---|---|---|---|---|
| 3 days | | | | scale/hold/rollback |
| 7 days | | | | scale/hold/rollback |
| 14 days | | | | scale/hold/rollback |

## Recommended Action Prioritization

Score each action qualitatively:

- Expected impact: high, medium, low.
- Confidence: high, medium, low.
- Urgency: immediate, this week, watch.
- Reversibility: easy, moderate, hard.
- Rank/velocity risk: protects rank, neutral, risks rank.
- Gate status: passed, blocked, or watch.

Recommended actions should usually fall into one of these groups:

- Restore lost proven traffic.
- Reallocate spend from weak routes to proven high-intent routes.
- Harvest converting search terms or ASINs into controlled campaigns.
- Add negatives only for current, material, non-strategic waste.
- Adjust bids/placements where the driver is traffic quality, CPC, or lost placement.
- Fix offer/listing/price/coupon/stock before scaling traffic when CVR fell broadly.
- Run a focused relaunch when old campaign history or structure is contaminated.

## Verification Plan

Use these checkpoints:

- 3 days: confirm impressions/clicks/order velocity moved in the intended direction; watch CPC and spend pacing.
- 7 days: confirm CVR, sales/orders per day, ACOS/ROAS/TACoS when valid, and BSR response; decide whether to scale, hold, or rollback.
- 14 days: confirm sustained BSR/organic momentum and whether corrected campaigns are replacing lost volume without moving waste elsewhere.

Define specific thresholds when data permits, such as target CPC, minimum orders, CVR floor, ACOS ceiling, ROAS floor, TACoS ceiling, BSR range, spend cap, or budget pacing target.
