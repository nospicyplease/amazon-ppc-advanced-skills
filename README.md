# Amazon PPC Advanced Skills

Reusable Codex skills for advanced Amazon PPC diagnosis, profitable growth opportunity discovery, and account-level growth orchestration.

This repository contains three complementary skills:

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

## Who This Is For

- Amazon brand operators.
- Amazon PPC specialists.
- Marketplace growth managers.
- Agencies managing multiple Amazon accounts.
- Analysts converting Amazon Ads, Business Reports, BSR, and retail-readiness data into action plans.

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

docs/
  INSTALLATION.md
  SKILL_CATALOG.md
  OPERATING_WORKFLOW.md
  MAINTENANCE.md
```

## Install Locally

Copy the skill folders into your Codex skills directory:

```bash
cp -R amazon-ads-performance-drop-diagnosis ~/.codex/skills/
cp -R amazon-growth-opportunity-finder ~/.codex/skills/
cp -R amazon-account-growth-operating-system ~/.codex/skills/
```

Restart or reload Codex so the skills list refreshes.

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for validation commands and update workflow.

## Recommended Usage

Use the skills in this order for a full account review:

1. Run `$amazon-ads-performance-drop-diagnosis` when there is any decline, risk, anomaly, or performance break.
2. Run `$amazon-growth-opportunity-finder` to identify profitable growth candidates.
3. Run `$amazon-account-growth-operating-system` to merge both outputs into one prioritized action plan.

For a single prompt:

```text
Use $amazon-account-growth-operating-system to combine the latest performance-drop findings and growth-opportunity findings into a weekly Amazon account action plan. Prioritize profitable growth, protect BSR, and flag all actions requiring approval.
```

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Skill catalog](docs/SKILL_CATALOG.md)
- [Operating workflow](docs/OPERATING_WORKFLOW.md)
- [Maintenance and update guide](docs/MAINTENANCE.md)

## Safety Notes

These skills do not execute Amazon Ads mutations by themselves. If connected to a live execution environment, all material write actions should remain approval-gated, preflighted against current live state, and verified with readback.

