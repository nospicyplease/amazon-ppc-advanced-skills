# Prompt

Use `$rocketcart-amazon-ads-live-review` to run a Product-Aware Growth Review for profile `example_de`.

Please use Rocketcart MCP if available as the Amazon Ads + product-intelligence connection. Inspect live campaigns, product ads and ASIN/SKU mapping, data freshness/quality, category/BSR movement, product context, inventory or availability blockers, Featured Offer / Buy Box risk, competitor/product signals, recent budget changes, live changes since the latest optimization snapshot, and snapshots/changelogs.

Classify each ASIN/campaign as Grow, Fix Before Scaling, Protect, Monitor, or Blocked. I specifically want to know which efficient campaigns are still unsafe to scale because of product context.

Produce proposed action rows only. Do not execute any bid, budget, placement, negative, product-ad state, target state, pause, relaunch, or campaign-creation writes.

For every proposed write, include exact entity IDs when available, current value, proposed value, expected impact, risk, preflight checks, approval requirement, readback plan, and monitoring window.
