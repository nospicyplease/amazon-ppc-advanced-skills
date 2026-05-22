# Input Summary

## Scope

- Rocketcart profile: `example_de`.
- Marketplace: DE.
- Ad type: Sponsored Products.
- Review type: Product-Aware Growth Review, no writes.
- Goal: classify campaigns and ASINs as Grow, Fix Before Scaling, Protect, Monitor, or Blocked before proposing approval-gated action rows.

## First-Run Behavior

- If Rocketcart MCP is available, use it to read live state and cross-check the fixture assumptions.
- If Rocketcart MCP is unavailable, run standalone from the provided fixture files and state that live preflight/readback are unavailable.
- In both modes, do not execute writes. Treat all action rows as proposed, blocked, monitor-only, or approval-required.

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
- Complete competitor history.
- Product context for `rc-camp-1006`.
- Confirmation of final human-approved action rows.

## Assumptions

- Initial review is read-only.
- Writes are not allowed without a separate explicit approval step.
- Any proposed action that lacks exact IDs or preflight is not executable.
- Product context can block scale even when ACoS, ROAS, or conversion look efficient.
