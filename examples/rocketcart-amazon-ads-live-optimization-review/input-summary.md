# Input Summary

## Scope

- Rocketcart profile: `example_de`.
- Marketplace: DE.
- Ad type: Sponsored Products.
- Review type: live read-first review, no writes.
- Goal: identify safe optimization actions and live-state risks.

## Available Live Reads To Use When MCP Is Available

- `list_campaigns` for enabled SP campaign state, budgets, bidding strategy, and placement modifiers.
- `detect_budget_changes` for the last 30 days.
- `detect_live_changes` compared with the latest optimization snapshot.
- `list_snapshots` for optimization snapshots and changelogs.
- `get_profile_mcp_context` only if planning approved execution context, not as approval.

## Static Context Provided By User

- Target ACoS by product group.
- Known inventory blockers for two ASINs.
- Summary of last week's intended optimization plan.
- Current business goal: controlled growth with no inventory-risk scaling.

## Missing Data

- Full search term report.
- BSR and total retail sales.
- Competitor data.
- Confirmation of final human-approved action rows.

## Assumptions

- Initial review is read-only.
- Writes are not allowed without a separate explicit approval step.
- Any proposed action that lacks exact IDs or preflight is not executable.
