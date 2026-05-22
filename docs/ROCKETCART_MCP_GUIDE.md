# Rocketcart MCP Guide

Rocketcart MCP is the optional live connection layer for these skills. It connects Amazon Ads state with product intelligence so an agent can move from static PPC reasoning to product-aware, approval-gated optimization review.

## The Plain-English Version

Standalone skills answer: "What does this exported Amazon PPC data suggest?"

Rocketcart MCP answers: "What does the live Amazon Ads account show right now, what product context changes the decision, what has already been changed, and which actions are safe enough to ask a human to approve?"

## What Rocketcart MCP Adds

| Layer | What It Contributes | Why It Matters |
|---|---|---|
| Amazon Ads live state | Profiles, campaigns, budgets, states, bidding strategy, placement modifiers, product ads, keyword/target bids, negatives, and campaign creation surfaces where available | Prevents acting on stale exports or wrong entities |
| Ads analytics | Profile, campaign, placement, targeting, search-term, waste, ASIN, and health signals | Grounds recommendations in recent performance and data quality |
| Product intelligence | Category rank/BSR movement, price, estimated demand, stock/availability signals, rating/reviews, Featured Offer / Buy Box, competitor signals, and seasonal context where available | Prevents scaling products that cannot safely convert or fulfill demand |
| Recent-change context | Snapshots, changelogs, prior entity history, pending evaluations, cooldowns, and live drift | Prevents repeating recent losing actions or touching entities already under evaluation |
| Guarded execution | Preflight, exact entity IDs, approval packets, writes, readback, and monitoring | Keeps live changes human-approved and auditable |

This repository does not install or configure Rocketcart MCP. It teaches Codex or Claude how to use Rocketcart MCP when that capability layer is already available in the host environment.

## What Comes From Rocketcart Vs The User

| Need | Standalone Mode | Rocketcart MCP Mode |
|---|---|---|
| Amazon Ads campaign state | User exports/pastes reports | Read live with Rocketcart campaign, product-ad, and snapshot/drift capabilities |
| Budget or placement drift | User change log or reports | Read with Rocketcart budget, live-drift, and targeting-change capabilities |
| Product intelligence | User provides BSR, inventory, price, reviews, margin, readiness exports | Read or cross-check where available with category/BSR, product-vs-ads, competitor, product health, and ASIN-level control reads |
| Data freshness/quality | User states report windows | Read with freshness and quality checks where available |
| Recent-change context | User notes recent changes | Read from snapshots, changelogs, entity history, and pending evaluations |
| Live writes | Not available | Available only after approval, preflight, exact IDs, readback, and monitoring |

If Rocketcart context is unavailable, the skill must say so, lower confidence, and fall back to static-export reasoning.

## Product Intelligence Context

Rocketcart product intelligence is the reason this bridge is more than an Amazon Ads connector. A product-aware PPC review should check:

- ASIN and SKU mapping from product ads.
- Inventory, availability, stock risk, or days of supply when available.
- Featured Offer / Buy Box status or offer risk.
- Category rank/BSR movement, price, estimated demand, rating, and review context.
- BSR history, BSR versus ads, and BSR responsiveness when rank is part of the goal.
- Competitor health signals such as price drops, stock-outs, Buy Box changes, and deals.
- Product-level ads performance and ASIN KPI control checks.
- Margin, target ACoS, target CPA, fees, returns, or product economics when available from the user or Rocketcart context.

Product intelligence can block otherwise attractive PPC actions. A campaign can be efficient and still be unsafe to scale when stock is low, Featured Offer is unstable, price is uncompetitive, reviews are weak, or BSR movement is not actually responsive to ads.

## Common Rocketcart MCP Reads

Exact capabilities can vary by host. When present, these reads are the main bridge:

### Profile And Live Ads State

- Profile discovery when the profile is missing.
- SP campaign budgets, states, targeting type, bidding strategy, and placement modifiers.
- Advertised ASIN/SKU mapping to campaign and ad group IDs.
- Marketplace bid guidance before bid changes.

### Change And Memory Context

- Recent budget changes.
- Live Ads state compared with the latest optimization snapshot.
- Keyword/target bid or state changes from snapshots.
- Negative keyword changes between snapshots.
- Optimization snapshots and changelogs.
- Prior optimization events.
- Entity history for a campaign, keyword, target, or other entity ID.

### Product Intelligence

Rocketcart MCP may expose product-intelligence reads for:

- Profile, campaign, budget, waste, placement, ASIN, search-term, and report-quality signals.
- ASIN-scoped KPI precision and mixed-ASIN risk.
- Category rank/BSR, price, estimated demand, offer status, and freshness.
- Product metrics compared with SP ACoS/ROAS.
- Daily BSR alongside impressions, clicks, spend, sales, ACoS, and ROAS.
- BSR responsiveness, lag, momentum, and confounders.
- Seasonal BSR, demand, and price patterns where enough history exists.
- Competitor price, stock, Featured Offer / Buy Box, and deal changes.

## First Rocketcart Review Prompt

```text
Use $rocketcart-amazon-ads-live-optimization-review for profile example_de.

Run a read-first Amazon Ads + product-intelligence review. Confirm the profile, inspect live Sponsored Products campaigns, product ads/ASIN mapping, recent budget and targeting drift, snapshots/changelogs, data freshness/quality, category/BSR movement, product context, inventory or availability blockers, Featured Offer / Buy Box risk, and competitor/product signals where available.

Produce proposed action rows only. Do not execute any bid, budget, placement, negative, pause, relaunch, product-ad, target, or campaign-creation write. Any write candidate must include exact IDs, current value, proposed value, expected impact, risk, approval requirement, live preflight, readback, and 3/7/14-day monitoring.
```

## Product-Aware Growth Prompt

```text
Use Rocketcart MCP with $amazon-growth-opportunity-finder and $rocketcart-amazon-ads-live-optimization-review to find product-aware growth opportunities.

For each ASIN or campaign, join Amazon Ads performance with product context: inventory/availability, Featured Offer / Buy Box, price, reviews/rating, category rank/BSR movement, estimated demand, BSR responsiveness, competitor movement, margin or target ACoS, recent changes, and recent optimization context. Classify each opportunity as Grow, Fix Before Scaling, Protect, Monitor, or Blocked.

Keep all live write actions approval-gated. Do not execute.
```

## Approval And Execution Boundary

Rocketcart MCP may expose write capabilities, but availability is not permission.

Any bid, budget, placement, negative, product-ad state, target state, pause, relaunch, campaign creation, or other live write requires:

- Explicit human approval for the exact row or approval packet.
- Exact Amazon Ads entity IDs.
- Live preflight against current state.
- Current value and proposed value.
- Expected impact and primary risk.
- Product-readiness check when the action could affect product demand, rank, or stock.
- Readback after execution.
- Monitoring window with success and failure criteria.

If any requirement is missing, the action is not executable.

## How To Explain Rocketcart To A New User

Rocketcart MCP is the live, product-aware operating layer:

- It connects the assistant to live Amazon Ads state.
- It adds product intelligence so PPC recommendations know whether the product can actually support more traffic.
- It remembers recent optimization actions and checks live drift.
- It turns recommendations into approval-ready rows.
- It only executes live writes after human approval, preflight, readback, and monitoring.
