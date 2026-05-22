# Rocketcart MCP Tool Map

Use this reference when Rocketcart MCP tools are available. Tool names may appear with a namespace in the host environment, but the skill should reason about the operations below.

## Read Tools

- `list_profiles`: list available Amazon Ads profiles with slug, profile ID, country, and API region. Use first when the user did not specify a profile.
- `list_campaigns`: inspect SP campaigns, including budget, state, targeting type, bidding strategy, and placement modifiers.
- `detect_budget_changes`: detect recent day-over-day campaign budget changes from report snapshots.
- `detect_live_changes`: compare current API state against the most recent optimization snapshot for budgets, placements, keyword bids, and product-target bids.
- `list_snapshots`: list optimization snapshots and changelogs.
- `get_profile_mcp_context`: get official Amazon MCP routing context for a profile when planning approved writes.

## Write Tools

Never call these during the initial review. Use only after explicit approval, live preflight, exact IDs, and a readback plan.

- `update_campaign_budget`: update an SP campaign daily budget.
- `update_keyword_bids`: update SP keyword bids.
- `update_placement_modifiers`: update SP placement bid modifiers.
- `create_negative_keywords`: create campaign-level or ad-group-level negative keywords.
- `delete_negatives`: archive SP negative keywords by ID.
- `create_campaigns_now`: create campaigns immediately through the Amazon Ads API; use `dry_run` for validation where available before any real creation.

## Tool Use Examples

List profiles when profile is missing:

```text
list_profiles()
```

Then ask the user to choose when more than one profile plausibly matches the request. Do not infer from country or name alone when multiple profiles are possible.

Inspect live campaigns after profile is confirmed:

```text
list_campaigns(profile: "example_profile")
detect_budget_changes(profile: "example_profile")
detect_live_changes(profile: "example_profile")
list_snapshots(profile: "example_profile")
```

Preflight a budget action by checking at least:

- Profile and marketplace.
- Exact campaign ID.
- Current campaign state.
- Current budget.
- Recent budget or placement drift.
- Inventory, Featured Offer / Buy Box, margin, and strategic role.

If any field differs from the approved row, the approval is stale.

## Preflight By Action Type

Budget change:

- Confirm profile, campaign ID, campaign state, current budget, current spend/pacing context, recent budget changes, and whether the campaign is strategically defensive or rank-supporting.
- Block if inventory, Featured Offer / Buy Box, margin, or conversion risk makes the budget increase unsafe.

Keyword bid change:

- Confirm keyword ID, campaign/ad group, match type, current bid, current state, recent bid drift, performance evidence, and whether the term is branded, defensive, launch, rank-supporting, or exploratory.
- Block if sample size is weak or the proposed change depends on missing margin or retail readiness.

Placement modifier change:

- Confirm campaign ID, current placement modifiers, placement performance, CPC/CVR difference, recent placement drift, and strategic role.
- Block if placement data is too thin or the campaign mixes incompatible traffic types.

Negative keyword creation:

- Confirm search term, match type, campaign ID, ad group ID when ad-group-level, current waste evidence, relevance, and strategic role.
- Block if the term could be brand defense, own-ASIN defense, launch/rank defense, or a profitable low-volume term.

Negative deletion:

- Confirm negative keyword ID, current negative scope, reason to restore traffic, and risk of reopening waste.

Campaign creation:

- Confirm plan JSON, campaign objective, advertised ASINs, budgets, bids, targeting, negatives, portfolio, naming, launch state, and retail-readiness gates.
- Prefer dry run or validation first when the tool supports it.

## Readback

After an approved write, read back the affected entity:

- Campaign budget or state: use `list_campaigns`.
- Placement modifiers: use `list_campaigns`.
- Live drift from snapshot: use `detect_live_changes` when useful.
- Negative creation/deletion or keyword bid readback: use the available Rocketcart or Amazon MCP read path in the host environment.

Report what changed, what did not change, and what must be monitored over 3, 7, and 14 days.

## Failure Modes

Profile ambiguity:

- If multiple profiles match the user's request, list the candidates and ask the user to pick one.
- Do not inspect or execute against a guessed profile.

Missing IDs:

- Campaign names, keyword text, and search terms are not enough for live writes.
- Classify the row as `Needs IDs` until the exact Amazon Ads entity IDs are known.

Stale snapshot or changelog:

- Treat old snapshots as context, not approval.
- Refresh live state before any execution decision.

Current value mismatch:

- If live preflight shows a current bid, budget, placement modifier, negative state, or campaign state that differs from the approved row, do not execute.
- Produce a refreshed row and request refreshed approval for the new current/proposed pair.

Dry-run failure:

- Treat dry-run errors as blockers until resolved.
- Report the error, affected entity, likely cause, and the safest next read or edit.

Dry run passes but business gate fails:

- API validation does not override inventory, Featured Offer / Buy Box, margin, or brand/rank-defense gates.
- Keep the row blocked or downgrade it to a controlled test when business risk is high.

Write tool available during initial review:

- Availability is not permission.
- Do not call write tools during initial review even when they are exposed in the environment.
