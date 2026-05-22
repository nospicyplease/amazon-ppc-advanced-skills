# Amazon PPC Advanced Skills

Open-source agent skills for advanced Amazon PPC diagnosis, profitable growth opportunity discovery, and account-level growth orchestration.

Use these skills standalone in Codex or Claude with exported Amazon Ads, Business Reports, BSR, inventory, and retail-readiness data. If you use Rocketcart MCP, the same operating logic can become a live read, preflight, approval, execution, and readback workflow.

This repository contains five complementary skills:

1. `amazon-ads-performance-drop-diagnosis`
   - Diagnoses why Amazon Ads, retail sales, BSR, conversion, TACoS, ROAS, or rank performance declined.
   - Protects sales velocity and organic momentum before recommending bid, budget, negative, pause, or relaunch actions.

2. `amazon-growth-opportunity-finder`
   - Finds ASIN, campaign, keyword, search term, product-target, placement, BSR, and organic-rank opportunities that can grow profitably.
   - Checks margin, incrementality, retail readiness, Featured Offer / Buy Box, inventory, reviews, conversion, and BSR context before scale.

3. `amazon-account-growth-operating-system`
   - Orchestrates the first two skills into a single account action queue.
   - Decides what to protect, fix, scale, reduce, harvest, launch, monitor, and approval-gate.
   - Produces daily, weekly, or monthly operating plans with monitoring rules and success/failure criteria.

4. `amazon-search-term-harvest-planner`
   - Finds search terms ready for exact-match harvesting from auto, broad, phrase, or discovery campaigns.
   - Checks relevance, orders, ACoS/CPA, margin fit, retail readiness, duplicate risk, and source/destination routing.
   - Blocks unsafe source negatives when traffic may be brand defense, own-ASIN defense, launch/rank support, or low-sample discovery.

5. `rocketcart-amazon-ads-live-optimization-review`
   - Runs a read-first Sponsored Products optimization review in standalone or Rocketcart MCP mode.
   - Uses Rocketcart MCP, when available, to inspect profiles, campaigns, budget changes, live drift, and snapshots before proposing actions.
   - Keeps bid, budget, placement, negative, pause, relaunch, and campaign-creation writes approval-gated with preflight and readback.

## Who This Is For

- Amazon brand operators.
- Amazon PPC specialists.
- Marketplace growth managers.
- Agencies managing multiple Amazon accounts.
- Analysts converting Amazon Ads, Business Reports, BSR, and retail-readiness data into action plans.
- AI builders creating agent workflows for marketplace operations.

## Core Philosophy

These skills are designed to avoid shallow "optimize campaigns" advice. They force the agent to:

- Protect current sales and BSR before scaling.
- Separate facts from hypotheses.
- Use T-1 anchored windows when current-day data may be incomplete.
- Keep Sponsored Products, Sponsored Brands, and Sponsored Display separated when data supports it.
- Treat BSR as category-relative and volatile.
- Avoid claiming ad-to-BSR causation without strong evidence.
- Require margin, inventory, Featured Offer / Buy Box, conversion, reviews, and listing readiness before aggressive scale.
- Convert recommendations into concrete, approval-ready actions with monitoring rules.

## Repository Layout

```text
amazon-ads-performance-drop-diagnosis/
  SKILL.md
  agents/openai.yaml
  references/drop-diagnosis-framework.md

amazon-growth-opportunity-finder/
  SKILL.md
  agents/openai.yaml

amazon-account-growth-operating-system/
  SKILL.md
  agents/openai.yaml

amazon-search-term-harvest-planner/
  SKILL.md
  agents/openai.yaml

rocketcart-amazon-ads-live-optimization-review/
  SKILL.md
  agents/openai.yaml
  references/rocketcart-mcp-tool-map.md

docs/
  INSTALLATION.md
  SKILL_CATALOG.md
  OPERATING_WORKFLOW.md
  MAINTENANCE.md

examples/
  amazon-ads-performance-drop-diagnosis/
  amazon-growth-opportunity-finder/
  amazon-account-growth-operating-system/
  amazon-search-term-harvest-planner/
  rocketcart-amazon-ads-live-optimization-review/

evals/
  safety-gate-check.md
  bsr-causality-check.md
  action-specificity-check.md
  missing-data-confidence-check.md
  rocketcart-write-gate-check.md

templates/
  amazon-ppc-skill-template/
    SKILL.md
    agents/openai.yaml

.github/
  ISSUE_TEMPLATE/

CONTRIBUTING.md
ROADMAP.md
```

## Install Locally

### Codex

Copy the skill folders into your local Codex skills directory:

```bash
cp -R amazon-ads-performance-drop-diagnosis ~/.codex/skills/
cp -R amazon-growth-opportunity-finder ~/.codex/skills/
cp -R amazon-account-growth-operating-system ~/.codex/skills/
cp -R amazon-search-term-harvest-planner ~/.codex/skills/
cp -R rocketcart-amazon-ads-live-optimization-review ~/.codex/skills/
```

Restart or reload Codex so the skills list refreshes.

### Claude

Claude users can upload skills through Claude's skill settings. Package the skill folder you want to use, including its `SKILL.md`, `agents/` metadata if useful, and any `references/` files.

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for validation commands and update workflow.

## Recommended Usage

Use the skills in this order for a full account review:

1. Run `$amazon-ads-performance-drop-diagnosis` when there is any decline, risk, anomaly, or performance break.
2. Run `$amazon-growth-opportunity-finder` to identify profitable growth candidates.
3. Run `$amazon-account-growth-operating-system` to merge both outputs into one prioritized action plan.
4. Run `$amazon-search-term-harvest-planner` when you want a focused search-term harvesting and routing plan.
5. Run `$rocketcart-amazon-ads-live-optimization-review` when you want a read-first Rocketcart MCP review against live SP campaign state, snapshots, and recent changes.

For a single prompt:

```text
Use $amazon-account-growth-operating-system to combine the latest performance-drop findings and growth-opportunity findings into a weekly Amazon account action plan. Prioritize profitable growth, protect BSR, and flag all actions requiring approval.
```

## Examples And Evals

Each production skill has an anonymized example under `examples/`:

- `prompt.md`: realistic prompt for the skill.
- `input-summary.md`: available fields, missing fields, assumptions, and scope.
- `expected-output-outline.md`: sections and safety behavior a good answer should include.

The `evals/` directory contains lightweight review prompts for safety gates, BSR causality, action specificity, missing-data confidence, and Rocketcart write gates. Contributors should run the nearest example and use the relevant eval prompts before opening a PR.

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Skill catalog](docs/SKILL_CATALOG.md)
- [Operating workflow](docs/OPERATING_WORKFLOW.md)
- [Maintenance and update guide](docs/MAINTENANCE.md)
- [Contributing](CONTRIBUTING.md)
- [Roadmap](ROADMAP.md)
- [Examples](examples)
- [Evaluation prompts](evals)

## Contributing

Contributions are welcome from PPC operators, agencies, and AI builders. Start with [CONTRIBUTING.md](CONTRIBUTING.md), copy the reusable template in `templates/amazon-ppc-skill-template/`, and check [ROADMAP.md](ROADMAP.md) for good first skill ideas.

Good contributions preserve the project stance: specific evidence, explicit confidence, retail-readiness gates, and no unsupported live execution.

## Rocketcart MCP

Rocketcart MCP is an optional execution layer. These open-source skills should stay useful with static exports, but Rocketcart can add:

- Live Amazon Ads reads.
- Budget, bid, placement, negative, and campaign-state preflight.
- Optimization snapshots and change detection.
- Approval-gated execution.
- Readback and monitoring after approved changes.

The first Rocketcart-aware skill is `rocketcart-amazon-ads-live-optimization-review`. It proposes action rows from live reads but does not execute writes by default.

## Safety Notes

These skills do not execute Amazon Ads mutations by themselves. If connected to a live execution environment, all material write actions should remain approval-gated, preflighted against current live state, and verified with readback.
