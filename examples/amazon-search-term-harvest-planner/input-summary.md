# Input Summary

## Scope

- Marketplace: US.
- Ad type: Sponsored Products.
- Current window: last 30 complete days.
- Goal: profitable search-term harvesting with safe routing.

## Available Data

- Search term report with campaign, ad group, search term, targeting, match type, impressions, clicks, spend, orders, sales, ACoS, ROAS, CPC, CTR, and CVR.
- Targeting report with existing keywords, match type, bids, states, and campaign/ad group IDs.
- Campaign structure with auto, broad, phrase, and exact campaigns by ASIN.
- Current negatives at campaign level.
- Product context for advertised ASINs: price, target ACoS, inventory, Featured Offer / Buy Box status, review count, rating, and delivery promise.
- Destination campaign state, exact IDs, budget status, and current negative conflicts for the synthetic examples.
- Traffic-role and lifecycle-stage labels for brand defense, own-ASIN/substitute ambiguity, competitor conquest, launch/rank, and category generic terms.

## Missing Data

- Purchased-product report.
- Organic keyword rank.
- Competitor price and BSR movement.
- Full contribution margin; target ACoS is available.
- Some destination IDs and ASIN relationship context are intentionally missing to force `NEEDS_DATA`.

## Assumptions

- Same-day data is excluded.
- Terms with fewer than 2 orders are not automatically harvest-ready.
- Source negatives require routing or waste evidence.
- Negative phrase is allowed only for clearly irrelevant query families.
- No row is `APPROVAL_READY` unless exact IDs, current/proposed values, duplicate checks, current negative checks, destination feasibility, preflight, readback, approval text, and monitoring criteria are present.
