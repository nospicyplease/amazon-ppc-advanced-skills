# Rocketcart Search-Term Harvest Mode

Use this reference when `amazon-search-term-harvest-planner` runs with Rocketcart MCP available. Keep public outputs focused on capability categories and operator decisions, not implementation details.

## Read Sequence

1. Confirm or discover the profile.
   - If no profile is supplied, list available profiles.
   - If multiple profiles plausibly match, ask the user to choose.
   - Do not inspect or execute against a guessed profile.
2. Read live campaign and ad group state for the search-term scope.
3. Read product ads and ASIN/SKU mapping when product context, own-ASIN defense, launch/rank, or mixed-ASIN risk matters.
4. Read existing keywords, product targets, negatives, bids, budgets, states, and destination campaign/ad group context where available.
5. Read recent drift, snapshots, changelogs, and entity history before trusting static rows.
6. Read product intelligence where available: inventory or availability, Featured Offer / Buy Box, price, reviews/rating, category rank/BSR movement, estimated demand, competitor signals, margin/readiness, and data freshness.

## Live Resolution

Live resolution should map candidate rows to exact profile, marketplace, campaign, ad group, keyword, target, negative, product-ad, ASIN, and destination IDs where applicable.

Mark the row below `APPROVAL_READY` when:

- A name or text value cannot be resolved to one exact live entity.
- Multiple live entities match.
- The exact keyword or target already exists.
- An existing exact exists but is paused, archived, budget-starved, or blocked by a negative.
- The destination campaign or ad group is paused, budget-starved, wrong-ASIN, or blocked by a negative.
- Current negative coverage is unknown.
- Product context is missing and could change the action.

## Preflight By Harvest Action

### Exact Keyword Harvest

- Confirm profile, marketplace, source campaign/ad group ID, destination campaign/ad group ID, normalized search term, match type, and proposed bid.
- Check duplicate exact keywords and close normalized variants.
- Check destination negatives and source negatives.
- Check destination state, budget headroom, ASIN fit, current bid guidance where available, and product readiness.
- Block if live state differs from the candidate row or the destination cannot receive traffic.

### Product Target Candidate

- Confirm ASIN relationship, product target destination, advertised ASIN/SKU fit, and duplicate product target coverage.
- Check whether the ASIN-like search term is own-ASIN defense, substitute, complement, or irrelevant.
- Block if ASIN relationship is unknown or if a negative would cut own-ASIN defense.

### Source Negative

- Confirm exact source campaign/ad group scope, negative match type, negative text, and current negative coverage.
- Confirm the term is safely captured elsewhere or is clear waste.
- Review blast radius before phrase negatives.
- Block negatives that could cut brand defense, own-ASIN defense, launch/rank support, competitor strategy, profitable discovery, or low-sample learning.

### Delivery Fix For Existing Exact

- Confirm existing keyword/target ID, state, bid, destination, budget, and negative conflicts.
- Prefer fixing the existing entity over creating a duplicate.
- Require approval for reactivation, bid changes, negative removal, or budget changes.

## Approval Packet

An approval packet must include:

- Row ID.
- Exact profile and marketplace.
- Entity IDs and names.
- Current value and proposed value.
- Proposed action and action family.
- Reason, expected impact, and primary risk.
- Product-readiness result.
- Duplicate check, current negative check, destination feasibility, and source-negative blast-radius result.
- Approval text the user can approve or reject.
- Readback checks.
- 3/7/14-day monitoring success and failure criteria.

## Execution And Readback

Execution is allowed only after the user explicitly approves exact row IDs or exact approval text.

Before execution:

- Re-run live preflight.
- Confirm current values still match the approved row.
- Block stale approvals and request refreshed approval.

After execution:

- Read back affected keywords, targets, negatives, bids, budgets, product-ad states, or campaign states.
- Report `executed`, `partially_applied`, `not_applied`, `readback_pending`, or `readback_failed`.
- Start monitoring for destination delivery, source traffic health, duplicate leakage, query drift, ACoS/CPA, ROAS, CVR, orders, and product-readiness changes.

## Failure Modes

- Profile ambiguity: ask for selection.
- Missing IDs: keep below `APPROVAL_READY`.
- Duplicate exact found live: block duplicate harvest and switch to delivery fix.
- Negative conflict found live: block destination routing until resolved.
- Current value mismatch: stale approval, no execution.
- Product context unavailable: block or downgrade product-sensitive actions.
- Write capability available during review: do not use it.
