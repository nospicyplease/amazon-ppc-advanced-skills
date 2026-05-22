---
name: rocketcart-amazon-ads-live-optimization-review
description: Use for read-first Amazon Sponsored Products optimization reviews that can run standalone from static exports or use Rocketcart MCP as an optional Amazon Ads plus product-intelligence layer. Guides Codex to inspect Rocketcart profiles, live SP campaigns, product ads/ASIN context, category rank/BSR movement, competitor signals, product readiness, budget and targeting drift, snapshots/changelogs, and proposed approval-gated action rows without executing writes by default.
---

# Rocketcart Amazon Ads Live Optimization Review

## Purpose

Initial review is read-only.

Review Amazon Sponsored Products accounts with a read-first, approval-gated operating model. Use static exports when Rocketcart MCP is unavailable. When Rocketcart MCP capabilities are available, use them as the Amazon Ads + product-intelligence connection: inspect live account state, campaign settings, product ads/ASIN mapping, product readiness, category rank/BSR movement, competitor signals, budget changes, live changes since optimization snapshots, and previous snapshots/changelogs before proposing actions.

MCP means Model Context Protocol: a structured way for an assistant to use external tools and data sources. See the repo [glossary](../docs/GLOSSARY.md) for definitions of MCP, preflight, readback, action gates, and exact entity IDs.

This skill is the bridge between open-source Amazon PPC reasoning and Rocketcart's live product-aware account layer. It should produce sharper recommendations because it can compare proposed actions against current Ads state, product context, and optimization memory, but it must not execute writes by default.

## Modes

### Standalone Mode

Use this mode when the user provides pasted data, CSVs, exports, screenshots, or summaries.

- State that Rocketcart MCP was not used.
- Build the best possible read-only review from provided campaign, search-term, targeting, placement, budget, BSR, retail-readiness, and economics data.
- Lower confidence when live state, current entity IDs, snapshots, or recent changes are unavailable.
- Do not present write actions as executable without live preflight.

### Rocketcart MCP Mode

Use this mode when Rocketcart MCP capabilities are available or the user asks for a Rocketcart live review.

- If `profile` is missing, use Rocketcart profile discovery first. If there is exactly one profile, use it; if there are multiple plausible profiles, ask the user which one to review.
- Inspect SP campaigns with the available live campaign-read capability, preferring enabled campaigns unless the user asks for paused/archived context.
- Inspect product ads and ASIN/SKU mapping with the available product-ad read capability when ASIN context matters.
- Inspect product intelligence, report freshness, and quality where available, including ASIN-level controls, category rank/BSR movement, product-vs-ads context, seasonality, and competitor signals.
- Detect recent budget changes and live changes since the latest optimization snapshot.
- Review targeting, negative, and entity changes when relevant.
- Review optimization snapshots, changelogs, and recent action history.
- When a write action would need live routing context, use that context only for the approval/preflight plan; do not use it as permission to execute.
- Read [rocketcart-mcp-capability-map.md](references/rocketcart-mcp-capability-map.md) when you need Rocketcart capability categories, write surfaces, and preflight/readback expectations.

## Required Inputs

Gather, derive, or mark unavailable:

- Marketplace, profile, account, currency, timezone, and Sponsored Products scope.
- Business goal: profit, revenue growth, BSR/rank support, launch, defense, waste reduction, or balanced growth.
- Current and comparison windows, preferably T-1 anchored when same-day data may be incomplete.
- Campaign state, budget, bidding strategy, placement modifiers, targeting type, and recent changes.
- Performance metrics: spend, sales, orders, ACoS, ROAS, impressions, clicks, CTR, CPC, CVR, budget usage, and placement performance when available.
- Search-term, targeting, advertised-product, purchased-product, product-ad, and placement data when available.
- Product intelligence and retail readiness: ASIN/SKU mapping, margin or target ACoS/CPA, inventory or availability, Featured Offer / Buy Box, price, reviews, rating, delivery promise, listing status, category rank/BSR movement, estimated demand, BSR responsiveness, competitor signals, total sales, and TACoS when available.
- Previous optimization snapshots, changelogs, live drift, and user-approved changes.

## Review Workflow

1. Establish mode and scope.
   - State whether the review is `Standalone` or `Rocketcart MCP`.
   - Print profile, marketplace, ad type scope, date windows, freshness, attribution caveats, and missing data.

2. Read current state.
   - In Rocketcart MCP mode, list or confirm the profile, inspect campaigns, product ads/ASIN context, product intelligence, report freshness/quality, budget changes, targeting or negative drift, live drift, and snapshots/changelogs.
   - In Standalone mode, map provided fields to the closest equivalent live-state concepts.

3. Identify risks before upside.
   - Flag budget cuts, bid/placement drift, out-of-budget winners, paused or changed winner campaigns, waste concentration, poor query mix, retail-readiness blockers, inventory or availability risk, Featured Offer / Buy Box risk, weak product intelligence coverage, missing margin, and low-confidence data.
   - Preserve the guardrails from `amazon-ads-performance-drop-diagnosis` and `amazon-growth-opportunity-finder` when the review overlaps with drop diagnosis or growth discovery.

4. Build proposed action rows.
   - Separate read-only findings from write candidates.
   - For every candidate, specify entity type, exact entity ID when available, current state, proposed state, reason, expected impact, risk, confidence, timing, approval status, preflight checks, readback checks, and monitoring window.

5. Keep execution separate.
   - Do not use write capabilities during the initial review.
   - If the user asks to execute, first restate the exact approved action rows and run live preflight.
   - Execute only the approved subset, then read back state and define monitoring.

## Write-Action Safety Rules

Any bid, budget, placement, negative, pause, archive, relaunch, or campaign-creation action requires all of the following:

- Explicit human approval for the exact action row.
- Live preflight against current state immediately before execution.
- Exact entity IDs, not names alone.
- Current value and proposed value.
- Expected impact and primary risk.
- Product-readiness check when the action may affect demand, BSR, stock, launch, harvesting, or product-level scale.
- Rollback or next-response guidance.
- Readback after execution.
- Monitoring window with success and failure criteria.

If any requirement is missing, classify the action as `Approval Required`, `Preflight Required`, `Needs IDs`, `Needs Data`, or `Monitor Only` rather than executable.

### Example Action Rows

Blocked write row:

| Entity Type | Entity ID | Name | Current State | Proposed Action | Reason | Expected Impact | Risk | Confidence | Preflight | Approval |
|---|---|---|---|---|---|---|---|---|---|---|
| Campaign budget | Missing | Branded Defense | Budget unknown | Increase daily budget | Strong branded ROAS in static export | Could reduce budget caps | Missing live budget and campaign ID | Low | Needs exact ID and current budget | Needs IDs |

Approval-ready but not executed row:

| Entity Type | Entity ID | Name | Current State | Proposed Action | Reason | Expected Impact | Risk | Confidence | Preflight | Approval |
|---|---|---|---|---|---|---|---|---|---|---|
| Campaign budget | 1234567890 | Nonbrand Exact - Core | Budget 40 EUR/day, campaign enabled | Increase to 55 EUR/day | T-1 complete data shows budget-capped profitable orders and inventory is safe | More eligible impressions and orders | CPC inflation or weaker marginal CVR | Medium | Recheck profile, campaign ID, budget, state, inventory, and recent drift immediately before execution | Explicit approval required; not executed |

Example approval text for the second row:

```text
Approve campaign budget change for entity ID 1234567890 from 40 EUR/day to 55 EUR/day after live preflight confirms the current value is still 40 EUR/day, campaign is enabled, inventory and Featured Offer are safe, and readback plus 3/7/14-day monitoring are reported.
```

## Output Format

Return these sections unless the user asks for a shorter version:

1. **Mode, Scope, And Data Coverage**: mode, profile/account, marketplace, windows, live-read status, snapshots reviewed, missing data, and confidence.
2. **Executive Verdict**: 3-6 bullets covering what to protect, what to scale or fix, what changed recently, and whether execution is safe.
3. **Live State And Change Review**: campaigns inspected, budget changes, live drift since snapshot, snapshot/changelog context, and any reconciliation caveats.
4. **Product Intelligence And Readiness**: ASIN/SKU mapping, inventory or availability, Featured Offer / Buy Box, category rank/BSR movement, price, reviews/rating, estimated demand, competitor signals, margin, and missing product context.
5. **Read-Only Findings**: risks, opportunities, anomalies, and missing data that do not require execution.
6. **Proposed Action Rows**: table with Entity Type | Entity ID | ASIN/SKU | Name | Current State | Proposed Action | Product Context | Reason | Expected Impact | Risk | Confidence | Preflight | Approval.
7. **Execution Gate**: which actions are blocked, which are approval-ready, and what exact approval text or decision is needed.
8. **Readback And Monitoring Plan**: readback checks after execution plus 3-day, 7-day, and 14-day monitoring rules.
9. **Missing Data / Next Reads**: data or Rocketcart reads that would improve confidence.

## Default Stance

Prefer `read`, `diagnose`, `propose`, `preflight`, `approve`, `execute`, `readback`, `monitor` in that order. The review is successful even when no writes are recommended.
