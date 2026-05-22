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

## Rocketcart-Aware Skills

Use `rocketcart-amazon-ads-live-review` as the broad account and product-aware bridge. Use `amazon-search-term-harvest-planner` directly when the job is specifically search-term harvesting, source-negative routing, product-target expansion, delivery fixes, or harvest-row execution.

| Skill / Review Mode | Use When | Output |
|---|---|---|
| `rocketcart-amazon-ads-live-review` / Live Optimization Review | You need a current live Sponsored Products review or want to reconcile static findings with current state. | Live-state findings, drift checks, and approval-gated action rows. |
| `rocketcart-amazon-ads-live-review` / Product-Aware Growth Review | You want to know which ASINs/campaigns can safely grow after product context is checked. | Grow, Fix Before Scaling, Protect, Monitor, or Blocked classifications. |
| `amazon-search-term-harvest-planner` / Live Harvest Review | You need exact search-term harvesting, product-target expansion, source-negative routing, or delivery-fix rows checked live. | Live-resolved harvest classifications, duplicate/negative/destination preflight, and approval packets. |
| `amazon-search-term-harvest-planner` / Execute Approved Rows | Exact harvest rows were explicitly approved. | Execute only approved row IDs, then read back affected entities and monitor outcomes. |
| Either Rocketcart-aware skill / Post-Change Readback / Monitoring Review | Approved changes have been made or need outcome review. | Readback status, early results, and 3/7/14-day monitoring plan. |

## 60-Second Smoke Test

Use this after installing the skill, even before Rocketcart MCP is connected:

```text
Use $rocketcart-amazon-ads-live-review in Live Optimization Review mode. I do not have Rocketcart MCP connected yet. Run in standalone mode and tell me the exact Amazon Ads and product data you need for a safe first review. Do not execute anything.
```

Expected shape:

```text
Mode: Standalone
Review mode: Live Optimization Review
Execution: no writes
Missing data: campaign metrics, search terms, product/ASIN context, inventory, offer status, margin, BSR/category movement, competitor signals, recent changes
Next step: provide exports or connect Rocketcart MCP
```

## What Comes From Rocketcart Vs The User

| Need | Standalone Mode | Rocketcart MCP Mode |
|---|---|---|
| Amazon Ads campaign state | User exports/pastes reports | Read live with Rocketcart campaign, product-ad, and snapshot/drift capabilities |
| Budget or placement drift | User change log or reports | Read with Rocketcart budget, live-drift, and targeting-change capabilities |
| Product intelligence | User provides BSR, inventory, price, reviews, margin, readiness exports | Read or cross-check where available with category/BSR, product-vs-ads, competitor, product health, and ASIN-level control reads |
| Data freshness/quality | User states report windows | Read with freshness and quality checks where available |
| Recent-change context | User notes recent changes | Read from snapshots, changelogs, entity history, and pending evaluations |
| Live writes | Not available | Available only after approval, preflight, exact IDs, readback, and monitoring |
| Search-term harvest preflight | Manual duplicate/negative/destination checks | Live resolution of profile, campaign/ad group, keyword/target, negative, destination, product-ad, and product context where available |

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
- Existing keyword, product-target, negative, and destination coverage for harvest candidates where available.
- Marketplace bid guidance before bid changes.

### Change And Recent-Action Context

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

Live Optimization Review:

```text
Use $rocketcart-amazon-ads-live-review for profile example_de.

Run a read-first Amazon Ads + product-intelligence review. Confirm the profile, inspect live Sponsored Products campaigns, product ads/ASIN mapping, recent budget and targeting drift, snapshots/changelogs, data freshness/quality, category/BSR movement, product context, inventory or availability blockers, Featured Offer / Buy Box risk, and competitor/product signals where available.

Produce proposed action rows only. Do not execute any bid, budget, placement, negative, pause, relaunch, product-ad, target, or campaign-creation write. Any write candidate must include exact IDs, current value, proposed value, expected impact, risk, approval requirement, live preflight, readback, and 3/7/14-day monitoring.
```

Product-Aware Growth Review:

```text
Use $rocketcart-amazon-ads-live-review in Product-Aware Growth Review mode for profile example_de.

For each ASIN or campaign, join Amazon Ads performance with product context: inventory/availability, Featured Offer / Buy Box, price, reviews/rating, category rank/BSR movement, estimated demand, BSR responsiveness, competitor movement, margin or target ACoS, recent changes, and recent optimization context. Classify each opportunity as Grow, Fix Before Scaling, Protect, Monitor, or Blocked.

Keep all live write actions approval-gated. Do not execute.
```

Preflight / Approval Readiness Review:

```text
Use $rocketcart-amazon-ads-live-review in Preflight / Approval Readiness Review mode for profile example_de.

Review these candidate action rows for exact entity IDs, current values, proposed values, product-readiness gates, expected impact, risk, approval text, readback, and monitoring. Mark each row Approval Ready, Needs IDs, Needs Current Value, Needs Product Context, Stale Approval, Blocked, or Monitor Only.

Do not execute anything.
```

Post-Change Readback / Monitoring Review:

```text
Use $rocketcart-amazon-ads-live-review in Post-Change Readback / Monitoring Review mode for profile example_de.

Review the approved changes from the last execution window, read back affected entities, compare expected versus current state, and classify each action as Readback Confirmed, Partially Applied, Not Applied, Monitoring, Worked, Failed, or Needs More Data.

Do not execute new writes.
```

Search-Term Live Harvest Review:

```text
Use $amazon-search-term-harvest-planner in Live Harvest Review mode for profile example_de.

Resolve live campaign/ad group/keyword/target/negative IDs, check duplicate exacts, current negatives, destination campaign/ad group feasibility, product-ad ASIN/SKU context, recent drift, snapshots/changelogs, and product readiness. Classify terms as Harvest Ready, Controlled Test, Scale Existing Exact / Delivery Fix, Product Target Candidate, Bid Down / Keep Learning, Negative Candidate, Watchlist, or Needs Data.

Produce approval-gated harvest rows only. Do not execute any keyword, target, negative, bid, budget, placement, product-ad, pause, or campaign write.
```

Search-Term Execute Approved Rows:

```text
Use $amazon-search-term-harvest-planner in Execute Approved Rows mode for profile example_de.

Approved rows: H-003 only. Before execution, rerun live preflight and confirm exact IDs, current values, proposed values, duplicate checks, current negative checks, destination feasibility, product readiness, approval text, readback checks, and 3/7/14-day monitoring. Execute only H-003 if preflight still matches the approved row. Read back the affected entity and report monitoring criteria.
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

For search-term harvesting, vague instructions such as "execute all recommendations" are not approval. Approval must identify exact row IDs or exact entity/action text, and live preflight must still match the approved current values.

## How To Explain Rocketcart To A New User

Rocketcart MCP is the live, product-aware operating layer:

- It connects the assistant to live Amazon Ads state.
- It adds product intelligence so PPC recommendations know whether the product can actually support more traffic.
- It remembers recent optimization actions and checks live drift.
- It turns recommendations into approval-ready rows.
- It only executes live writes after human approval, preflight, readback, and monitoring.
