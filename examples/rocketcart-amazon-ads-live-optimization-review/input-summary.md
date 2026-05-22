# Input Summary

## Scope

- Rocketcart profile: `example_de`.
- Marketplace: DE.
- Ad type: Sponsored Products.
- Review type: live read-first review, no writes.
- Goal: identify safe optimization actions, live-state risks, and product-readiness blockers.

## Available Live Reads To Use When MCP Is Available

- Enabled SP campaign state, budgets, bidding strategy, and placement modifiers.
- ASIN/SKU mapping and product-ad state.
- Product, category, BSR, ASIN-control, and competitor reads for product intelligence where available.
- Profile, campaign, ASIN, search-term, and report-quality signals.
- ASIN-scoped KPI precision and mixed-ASIN risk.
- Competitor price, stock, Featured Offer / Buy Box, and deal signals.
- Budget changes for the last 30 days.
- Live state compared with the latest optimization snapshot.
- Optimization snapshots and changelogs.
- Live routing context only if planning approved execution context, not as approval.

## Static Context Provided By User

- Target ACoS by product group.
- Known inventory blockers for two ASINs.
- Synthetic category/BSR/product readiness fixture in `sample-data/product-intelligence.json`.
- Summary of last week's intended optimization plan.
- Current business goal: controlled growth with no inventory-risk scaling.

## Missing Data

- Full search term report.
- Full BSR history and total retail sales.
- Competitor data.
- Confirmation of final human-approved action rows.

## Assumptions

- Initial review is read-only.
- Writes are not allowed without a separate explicit approval step.
- Any proposed action that lacks exact IDs or preflight is not executable.
