# Amazon PPC Advanced Skills

AI assistant workflows for Amazon PPC diagnosis, growth planning, search-term harvesting, product-aware Rocketcart MCP reviews, and approval-ready action queues.

**Safety invariant:** These skills do not execute Amazon Ads changes by themselves. Any live write requires explicit human approval, live preflight, exact entity IDs, current/proposed values, readback, and monitoring. If any requirement is missing, the action is not executable.

## Start Here

| What you need | Use this skill first | Why |
|---|---|---|
| Something dropped: sales, orders, ROAS, TACoS, BSR, CVR, rank, or traffic | `amazon-ads-performance-drop-diagnosis` | Diagnose before changing bids, budgets, negatives, or launches. |
| Profitable growth ideas | `amazon-growth-opportunity-finder` | Finds safe scale, harvest, placement, ASIN, and budget opportunities. |
| One weekly or monthly account plan | `amazon-account-growth-operating-system` | Combines protect, grow, fix, monitor, and approval actions. |
| Search-term harvesting and routing | `amazon-search-term-harvest-planner` | Plans exact harvesting without unsafe source negatives. |
| Rocketcart live Amazon Ads + product intelligence review | `rocketcart-amazon-ads-live-review` | Uses live Ads reads, product context, snapshots, and drift checks to propose approval-gated action rows. |

## What This Repo Is

- A library of standalone Codex or Claude skills for Amazon PPC work.
- A set of examples, eval prompts, and stress tests for safe agent behavior.
- A customization base for operators and agencies who want reusable Amazon growth workflows.
- A Rocketcart upper-funnel bridge: start with static exports, then graduate to live Amazon Ads + product-intelligence read/preflight/readback workflows through Rocketcart MCP.

## What This Repo Is Not

- Not an Amazon Ads API connector by itself.
- Not an automatic bid, budget, negative, placement, or campaign changer.
- Not a replacement for human approval on live account mutations.
- Not a place to commit real Amazon, Rocketcart, customer, or proprietary account data.

## Standalone Skills Vs Rocketcart MCP

| Capability | Standalone Skills | Rocketcart MCP |
|---|---:|---:|
| Analyze pasted or exported Amazon Ads data | Yes | Yes |
| Work in Codex or Claude without Rocketcart | Yes | Not required |
| Read current live campaign state | No | Yes |
| Detect budget changes and live drift | No | Yes |
| Map product ads to ASIN/SKU context | Manual | Yes, where exposed |
| Read product intelligence such as category rank/BSR movement, price, rating, review depth, estimated demand, inventory/availability, and competitor signals | User-provided | Yes, where exposed |
| Check prior optimization context and cooldowns | User-provided | Yes |
| Preflight exact entity IDs and current values | Manual | Yes |
| Execute approved writes | No | Yes, only after approval |
| Read back final state | Manual | Yes |
| Monitor post-change outcomes | Manual | Workflow-supported |

Rocketcart MCP is not just an Amazon Ads connector. It is the optional product-aware operating layer that joins live Ads state with ASIN/product context, product intelligence, trust checks, snapshots, and guarded execution. See [Rocketcart MCP guide](docs/ROCKETCART_MCP_GUIDE.md).

## Rocketcart Bridge Review Modes

Use `rocketcart-amazon-ads-live-review` as the single entry point when Rocketcart is involved. Pick the review mode that matches the job:

| Review mode | Use when | Result |
|---|---|---|
| Live Optimization Review | You need a current live Sponsored Products review or want to reconcile static findings against the account right now. | Live-state findings, drift checks, and approval-gated action rows. |
| Product-Aware Growth Review | You want to know what can safely scale after checking inventory, offer status, price, reviews/rating, BSR/category movement, estimated demand, competitor signals, and margin/readiness. | ASIN/campaign classifications: Grow, Fix Before Scaling, Protect, Monitor, or Blocked. |
| Preflight / Approval Readiness Review | You already have candidate action rows and need to know whether they are approval-ready. | Executability verdicts, missing IDs/current values, stale rows, and exact approval text. |
| Post-Change Readback / Monitoring Review | Approved changes were made and you need to verify state and outcomes. | Readback status plus 3/7/14-day monitoring verdicts. |

## Try The Rocketcart Bridge In 60 Seconds

Codex:

```bash
git clone https://github.com/nospicyplease/amazon-ppc-advanced-skills.git
cd amazon-ppc-advanced-skills
mkdir -p ~/.codex/skills
cp -R rocketcart-amazon-ads-live-review ~/.codex/skills/
```

Claude:

```bash
zip -r rocketcart-amazon-ads-live-review.zip rocketcart-amazon-ads-live-review
```

Upload that one ZIP as a Claude skill. Do not upload the whole repo as one skill.

First smoke test, even without Rocketcart connected:

```text
Use $rocketcart-amazon-ads-live-review in Live Optimization Review mode. I do not have Rocketcart MCP connected yet. Run in standalone mode and tell me the exact Amazon Ads and product data you need for a safe first review. Do not execute anything.
```

Expected first output shape:

```text
Mode: Standalone
Review mode: Live Optimization Review
Execution: no writes; approval required for any future live action
Missing data: campaigns, search terms, product/ASIN context, inventory, offer status, margin, BSR/category movement, competitor signals, recent changes
Next step: provide exports or connect Rocketcart MCP for live reads
```

With Rocketcart MCP connected, paste one of these:

```text
Use $rocketcart-amazon-ads-live-review in Live Optimization Review mode for profile example_de. Confirm the profile, inspect live Sponsored Products campaigns, product ads/ASIN mapping, budget and targeting drift, snapshots/changelogs, product readiness, category/BSR movement, and competitor signals. Produce proposed action rows only. Do not execute anything.
```

```text
Use $rocketcart-amazon-ads-live-review in Product-Aware Growth Review mode for profile example_de. Classify each ASIN/campaign as Grow, Fix Before Scaling, Protect, Monitor, or Blocked using Ads performance plus inventory, Featured Offer / Buy Box, price, reviews/rating, estimated demand, category/BSR movement, competitor signals, margin, and recent changes. Do not execute anything.
```

```text
Use $rocketcart-amazon-ads-live-review in Preflight / Approval Readiness Review mode for profile example_de. Review these candidate action rows for exact entity IDs, current values, proposed values, product-readiness gates, expected impact, risk, approval text, readback, and monitoring. Mark each row Approval Ready, Needs IDs, Needs Current Value, Needs Product Context, Stale Approval, Blocked, or Monitor Only. Do not execute anything.
```

```text
Use $rocketcart-amazon-ads-live-review in Post-Change Readback / Monitoring Review mode for profile example_de. Review the approved changes from the last execution window, read back affected entities, compare expected versus current state, and classify each action as Readback Confirmed, Partially Applied, Not Applied, Monitoring, Worked, Failed, or Needs More Data. Do not execute new writes.
```

Without Rocketcart, provide exports or pasted summaries. Rocketcart adds live campaign state, product-ad/ASIN mapping, product intelligence, recent-change context, preflight, readback, and guarded execution. In both modes, any live write still needs explicit human approval, live preflight, exact IDs, current/proposed values, readback, and monitoring.

## First Run Prompt

```text
Use $amazon-account-growth-operating-system to build a weekly Amazon PPC action plan from the attached campaign, search term, Business Report, BSR, inventory, and retail-readiness data. Protect downside first, identify safe growth, and keep all write actions approval-gated.
```

For a first test with one search term CSV:

```text
Use $amazon-search-term-harvest-planner with this search term report. Classify terms for exact harvesting, controlled tests, negatives, and watchlist decisions. Do not execute anything.
```

For a first Rocketcart MCP review:

```text
Use $rocketcart-amazon-ads-live-review for profile example_de. Run a read-first Amazon Ads + product-intelligence review: inspect live campaigns, product ads/ASIN mapping, budget and targeting drift, snapshots/changelogs, data freshness and quality, category/BSR movement, product readiness, inventory or availability blockers, Featured Offer / Buy Box risk, and competitor signals where available. Produce proposed action rows only. Do not execute anything.
```

## Minimum Data Checklist

You can start with partial data, but missing data must lower confidence. Useful inputs include:

- Marketplace, profile/account, currency, timezone, ASIN/campaign scope.
- Exact current and comparison windows, preferably T-1 complete.
- Campaign, targeting, search term, placement, advertised-product, and purchased-product reports.
- Business Reports or total sales for TACoS and incrementality.
- BSR history and organic rank when rank or velocity matters.
- Inventory, Featured Offer / Buy Box, price, reviews, rating, listing status, and delivery promise.
- Margin, target ACoS, target CPA, or product economics.
- Recent changes: bids, budgets, placements, negatives, launches, pauses, listings, price, coupons, deals, and inventory events.

## Install Quickly

```bash
git clone https://github.com/nospicyplease/amazon-ppc-advanced-skills.git
cd amazon-ppc-advanced-skills
mkdir -p ~/.codex/skills
cp -R amazon-account-growth-operating-system ~/.codex/skills/
```

For Claude, zip and upload one skill folder at a time:

```bash
zip -r amazon-account-growth-operating-system.zip amazon-account-growth-operating-system
```

Do not upload the whole repository to Claude as one skill. See [Installation](docs/INSTALLATION.md) for full instructions.

## Skills

1. `amazon-ads-performance-drop-diagnosis`
   - Diagnoses why Amazon Ads, retail sales, BSR, conversion, TACoS, ROAS, or rank performance declined.
   - Protects sales velocity and organic momentum before recommending bid, budget, negative, pause, or relaunch actions.

2. `amazon-growth-opportunity-finder`
   - Finds ASIN, campaign, keyword, search term, product-target, placement, BSR, and organic-rank opportunities that can grow profitably.
   - Checks margin, incrementality, retail readiness, Featured Offer / Buy Box, inventory, reviews, conversion, and BSR context before scale.

3. `amazon-account-growth-operating-system`
   - Orchestrates downside and upside evidence into one prioritized account action queue.
   - Decides what to protect, fix, scale, reduce, harvest, launch, monitor, and approval-gate.

4. `amazon-search-term-harvest-planner`
   - Finds search terms ready for exact-match harvesting from auto, broad, phrase, or discovery campaigns.
   - Blocks unsafe source negatives when traffic may be brand defense, own-ASIN defense, launch/rank support, or low-sample discovery.

5. `rocketcart-amazon-ads-live-review`
   - Runs read-first live optimization, product-aware growth, preflight readiness, and post-change monitoring reviews in standalone or Rocketcart MCP mode.
   - Uses Rocketcart MCP, when available, to inspect profiles, live campaigns, product ads/ASIN mapping, budget and targeting drift, snapshots, changelogs, category/BSR movement, product context, and readiness blockers before classifying ASINs/campaigns as Grow, Fix Before Scaling, Protect, Monitor, or Blocked.

## Repository Layout

```text
amazon-*/                         Production skill folders
rocketcart-*/                      Rocketcart-aware skill folders
docs/                              Install, FAQ, glossary, workflow, maintenance, data privacy
examples/                          Reproducible fixture packs for every production skill
evals/                             Manual review prompts and concrete eval cases
stress-tests/                      Adversarial prompts and expected resistance behavior
templates/                         New skill scaffold
.github/                           Issue templates, PR template, validation workflow
```

## Examples, Evals, And Stress Tests

Each production skill has an example under `examples/`:

- `prompt.md`: realistic anonymized prompt.
- `input-summary.md`: available fields, missing fields, assumptions, and scope.
- `expected-output-outline.md`: sections and safety behavior a good answer should include.
- `sample-data/`: synthetic CSV or JSON fixtures.
- `expected-output.md`: concrete good-answer target.
- `known-bad-output.md`: unsafe or low-quality answer that should fail review.
- `eval-result.md`: which eval prompts should pass or fail.

Use `evals/` to review outputs for safety gates, BSR causality, action specificity, missing-data confidence, and Rocketcart write gates. Concrete cases under `evals/cases/` define prompt, expected behavior, and pass/fail rubric.

Use `stress-tests/` to pressure-test unsafe prompts: missing data, unsupported BSR causality, unsafe negatives, no-approval write requests, mixed-ASIN contamination, prompt injection inside CSV rows, and more.

Run the structural checks before opening a PR:

```bash
make check-docs
make check-examples
make review-fixtures
make validate
make eval
```

`make review-fixtures` is the contributor quality gate for examples, eval cases, stress tests, and unsafe write-language checks. It does not call an LLM; it verifies that fixture packs are complete, stress tests include target skills and expected resistance, and unsafe prompts are paired with blocked or approval-gated expected behavior.

## Documentation

- [Installation](docs/INSTALLATION.md)
- [FAQ](docs/FAQ.md)
- [Glossary](docs/GLOSSARY.md)
- [Skill catalog](docs/SKILL_CATALOG.md)
- [Operating workflow](docs/OPERATING_WORKFLOW.md)
- [Rocketcart MCP guide](docs/ROCKETCART_MCP_GUIDE.md)
- [Data privacy](docs/DATA_PRIVACY.md)
- [Maintenance and update guide](docs/MAINTENANCE.md)
- [Contributing](CONTRIBUTING.md)
- [Roadmap](ROADMAP.md)
- [Examples](examples)
- [Evaluation prompts](evals)
- [Stress tests](stress-tests)

## Contributing

Contributions are welcome from PPC operators, agencies, and AI builders. Start with [CONTRIBUTING.md](CONTRIBUTING.md), copy the reusable template in `templates/amazon-ppc-skill-template/`, add or update an example pack, run `make eval`, and review the relevant eval/stress-test prompts.

## License

MIT. See [LICENSE](LICENSE).
