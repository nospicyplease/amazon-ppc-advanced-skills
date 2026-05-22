# Maintenance And Update Guide

## Editing Principles

- Keep each skill self-contained.
- Keep `SKILL.md` concise enough to load into context.
- Put detailed references in a `references/` directory only when needed.
- Do not duplicate large bodies of logic across skills unless the duplication is intentionally local and useful.
- Preserve approval gates for live write actions.
- Keep Amazon terminology current. Use `Featured Offer / Buy Box` when referring to offer ownership.
- Keep open-source skills useful with static exports; treat Rocketcart MCP as an optional live read, preflight, approval, execution, and readback layer.
- Keep examples and eval prompts aligned with skill behavior whenever a skill's output format, safety gates, or actionability rules change.

## Validation Checklist

Before committing updates:

1. Confirm every skill folder has `SKILL.md`.
2. Confirm every `SKILL.md` has valid frontmatter with only `name` and `description`.
3. Confirm `agents/openai.yaml` matches the skill name and purpose.
4. Confirm examples do not invent metrics or imply unsupported live execution.
5. Confirm the Growth Operating System still references both upstream skills correctly.
6. Confirm new skills are listed in `README.md` and `docs/SKILL_CATALOG.md` when they are user-facing.
7. Confirm each production skill has an example with `prompt.md`, `input-summary.md`, and `expected-output-outline.md`.
8. Review changed outputs with the relevant `evals/` prompt before opening a PR.
9. Validate all skills with `quick_validate.py` if available.

## Recommended Commands

```bash
find . -maxdepth 2 -name SKILL.md -print | sort
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./amazon-ads-performance-drop-diagnosis
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./amazon-growth-opportunity-finder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./amazon-account-growth-operating-system
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./amazon-search-term-harvest-planner
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./rocketcart-amazon-ads-live-optimization-review
```

To validate a new skill copied from the template:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./your-new-skill
```

Do not validate `templates/amazon-ppc-skill-template` as a production skill without first replacing the placeholder name, description, and body.

## Example And Eval Review

Use examples and evals as lightweight regression checks:

1. Pick the example closest to the skill or behavior you changed.
2. Run the example prompt against the changed skill instructions.
3. Compare the output with `expected-output-outline.md`.
4. Paste the output into relevant eval prompts:
   - `evals/safety-gate-check.md` for any execution recommendation.
   - `evals/bsr-causality-check.md` for BSR, rank, or organic-growth claims.
   - `evals/action-specificity-check.md` for proposed action rows.
   - `evals/missing-data-confidence-check.md` for partial data.
   - `evals/rocketcart-write-gate-check.md` for Rocketcart MCP write candidates.
5. Fix the skill or docs when an eval returns `Needs revision` or `Fail`.

## Release Notes Template

Use this structure in commit messages or release notes:

```text
Update Amazon PPC Advanced Skills

- Performance Drop Diagnosis:
- Growth Opportunity Finder:
- Growth Operating System:
- Documentation:
- Validation:
```

## Compatibility Notes

The Growth Operating System depends on the concepts and outputs of:

- `amazon-ads-performance-drop-diagnosis`
- `amazon-growth-opportunity-finder`

When either upstream skill changes its output structure, evidence thresholds, or action gates, review `amazon-account-growth-operating-system/SKILL.md` and update:

- Upstream execution order.
- Conflict resolution.
- Action gate transfer.
- Priority scoring.
- Output template.
- Human approval rules.
