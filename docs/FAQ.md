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

MCP means Model Context Protocol. It lets an AI assistant use external tools and data sources through a structured interface.

## Do I need Rocketcart?

No. The skills work standalone with static exports, pasted CSVs, or summaries. Rocketcart MCP adds live reads, snapshots, preflight, approval-gated execution, and readback.

## Can this change my Amazon Ads account?

Not by itself. These open-source skills do not execute Amazon Ads changes. Any live write requires explicit approval, live preflight, exact entity IDs, current/proposed values, readback, and monitoring.

## Which skill should I start with?

- Performance got worse: `amazon-ads-performance-drop-diagnosis`.
- You want growth ideas: `amazon-growth-opportunity-finder`.
- You want one weekly plan: `amazon-account-growth-operating-system`.
- You have a search term CSV: `amazon-search-term-harvest-planner`.
- You use Rocketcart MCP: `rocketcart-amazon-ads-live-optimization-review`.

## Which Amazon reports should I export?

Useful reports include campaign, targeting, search term, placement, advertised-product, purchased-product, Business Reports, BSR/rank history, inventory/offer data, retail-readiness data, and recent change history.

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

The repo is usable, but it can still improve with sample CSV fixtures, known-good outputs, automated evals, more Rocketcart examples, and more specialist skills.
