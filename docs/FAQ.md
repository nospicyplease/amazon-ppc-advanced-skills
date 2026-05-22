# FAQ

This FAQ is for first-time visitors from GitHub, Codex, Claude, or Rocketcart. See [Glossary](GLOSSARY.md) for definitions of PPC and platform terms.

## What is this repository?

It is a library of Amazon PPC agent skills. Each skill is a folder with a `SKILL.md` file that tells Codex or Claude how to perform a specific Amazon Ads workflow.

## Is this a software package?

No. There is no app server or dependency install. The repo contains skills, examples, eval prompts, stress tests, and documentation.

## What is a Codex skill?

A Codex skill is a folder with a `SKILL.md` file that gives Codex specialized instructions. Copy one skill folder into `~/.codex/skills/`, then reload Codex.

## What is a Claude skill?

A Claude skill is a skill folder uploaded to Claude. Zip and upload one skill folder at a time. Do not upload this whole repository as one skill.

## What is MCP?

MCP means Model Context Protocol. It lets an AI assistant use approved external context and action capabilities through a structured interface.

## Do I need Rocketcart?

No. The skills work standalone with static exports, pasted CSVs, or summaries. Rocketcart MCP adds live Amazon Ads reads, product intelligence, snapshots, recent-change context, preflight, approval-gated execution, and readback.

## How do I test the Rocketcart bridge after installing it?

Paste this into Codex or Claude:

```text
Use $rocketcart-amazon-ads-live-review in Live Optimization Review mode. I do not have Rocketcart MCP connected yet. Run in standalone mode and tell me the exact Amazon Ads and product data you need for a safe first review. Do not execute anything.
```

A good first output should say it is in standalone mode, list missing campaign/product data, refuse execution, and ask for exports or a Rocketcart MCP connection for live reads.

For search-term-specific Rocketcart testing, use:

```text
Use $amazon-search-term-harvest-planner in Live Harvest Review mode for profile example_de. Resolve live campaign/ad group/keyword/negative IDs, check duplicate exacts, current negatives, destination feasibility, product-ad ASIN/SKU context, recent drift, and product readiness. Produce approval-gated harvest rows only. Do not execute anything.
```

## Is Rocketcart MCP just an Amazon Ads connector?

No. Rocketcart MCP is the optional Amazon Ads + product-intelligence connection. It can expose live campaign state and product context such as ASIN/SKU mapping, category rank/BSR movement, price, estimated demand, rating/reviews, stock or availability, Featured Offer / Buy Box risk, competitor signals, recent-change context, and data freshness/quality signals where those reads are available.

## What if Rocketcart product-intelligence context is unavailable?

The skill should say which context is unavailable, lower confidence, and fall back to static exports or user-provided product data. Missing product context should block or downgrade risky scale, launch, pause, or negative recommendations.

## What do I provide in standalone mode?

Provide the best available exports or summaries: campaign, targeting, search term, placement, advertised-product, purchased-product, Business Reports, BSR/category movement, inventory or availability, Featured Offer / Buy Box, price, reviews/rating, margin or target ACoS, competitor signals, and recent changes.

## What does Rocketcart MCP add?

When available, Rocketcart MCP can read or cross-check live campaign state, product-ad/ASIN mapping, product intelligence, recent-change context, snapshots, preflight state, and readback. It still does not remove the need for human approval before any live write.

## Can this change my Amazon Ads account?

Not by itself. These open-source skills do not execute Amazon Ads changes. Any live write requires explicit approval, live preflight, exact entity IDs, current/proposed values, readback, and monitoring.

## Which skill should I start with?

- Performance got worse: `amazon-ads-performance-drop-diagnosis`.
- You want growth ideas: `amazon-growth-opportunity-finder`.
- You want one weekly plan: `amazon-account-growth-operating-system`.
- You have a search term CSV: `amazon-search-term-harvest-planner`.
- You use Rocketcart MCP for live Ads + product context: `rocketcart-amazon-ads-live-review`.
- You use Rocketcart MCP specifically for search-term harvesting, source negatives, or product-target expansion: `amazon-search-term-harvest-planner`.

## Which Amazon reports should I export?

Useful reports include campaign, targeting, search term, placement, advertised-product, purchased-product, Business Reports, BSR/rank history, inventory/offer data, retail-readiness data, and recent change history. With Rocketcart MCP, some of this context may be read live or cross-checked through product-intelligence capabilities.

## Can I paste CSVs?

Yes. You can paste CSV text, upload files when your AI environment supports it, or summarize data. Missing fields should lower confidence.

## Does this support Sponsored Products, Sponsored Brands, and Sponsored Display?

Yes, but coverage varies by skill and by data availability. Sponsored Products is the strongest path today, especially for the Rocketcart live-review skill. The skills should separate SP, SB, and SD whenever the data supports it.

## What happens if margin is missing?

The skill should avoid firm profitability claims. It may use ACoS, ROAS, or CPA as proxies and mark confidence lower.

## What happens if total sales is missing?

The skill should avoid TACoS, incrementality, and ad-dependency conclusions.

## What happens if BSR is missing?

The skill should avoid rank-growth claims and focus on ads and retail-readiness signals.

## What happens if inventory or Featured Offer / Buy Box is missing?

The skill should not assume scale readiness. Aggressive bid or budget increases should be blocked or downgraded.

## Where do I learn the Rocketcart flow?

Read [Rocketcart MCP guide](ROCKETCART_MCP_GUIDE.md). It explains what Rocketcart adds, which context can come from Rocketcart versus the user, first-run prompts, product-aware review prompts, search-term harvest prompts, and the execution boundary.

## Why not just cut high ACoS or zero-order spend?

High ACoS can be strategic during launch, rank defense, competitor conquesting, or brand defense. Zero-order spend may be low-sample discovery. The skills should only recommend cuts when waste is isolated and not protecting a strategic goal.

## How do I know the output is good?

Use:

- `examples/` to see expected structure.
- `evals/` to review safety, BSR causality, action specificity, missing-data confidence, and Rocketcart write gates.
- `stress-tests/` to pressure-test unsafe or overconfident behavior.

## Can agencies use this commercially?

Yes, subject to the MIT license. Do not commit client data or proprietary Rocketcart/customer data.

## How do I contribute?

Start from `templates/amazon-ppc-skill-template/`, keep the skill narrow, add an example pack, update the catalog and README, run validation, and review relevant eval/stress-test prompts. See [Contributing](../CONTRIBUTING.md).

## What is still missing?

The repo is usable, but it can still improve with deeper automated eval scoring, more Rocketcart product-intelligence examples, and more specialist skills.
