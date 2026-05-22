# Maintenance And Update Guide

## Editing Principles

- Keep each skill self-contained.
- Keep `SKILL.md` concise enough to load into context.
- Put detailed references in a `references/` directory only when needed.
- Do not duplicate large bodies of logic across skills unless the duplication is intentionally local and useful.
- Preserve approval gates for live write actions.
- Keep Amazon terminology current. Use `Featured Offer / Buy Box` when referring to offer ownership.
- Keep open-source skills useful with static exports; treat Rocketcart MCP as an optional live read, preflight, approval, execution, and readback layer.
- Keep Rocketcart docs clear that MCP is the Amazon Ads + product-intelligence connection, not only a live campaign-state connector.
- Keep examples, eval prompts, and concrete eval cases aligned with skill behavior whenever a skill's output format, safety gates, or actionability rules change.
- Keep stress tests aligned with the most important ways a skill could become unsafe or overconfident.

## Validation Checklist

Before committing updates:

1. Confirm every skill folder has `SKILL.md`.
2. Confirm every `SKILL.md` has valid frontmatter with only `name` and `description`.
3. Confirm `agents/openai.yaml` matches the skill name and purpose.
4. Confirm examples do not invent metrics or imply unsupported live execution.
5. Confirm the Growth Operating System still references both upstream skills correctly.
6. Confirm new skills are listed in `README.md` and `docs/SKILL_CATALOG.md` when they are user-facing.
7. Confirm each production skill has an example with `prompt.md`, `input-summary.md`, `expected-output-outline.md`, `sample-data/`, `expected-output.md`, `known-bad-output.md`, and `eval-result.md`.
8. Confirm new-user docs answer what the skill is, how to install it, what data is needed, and whether live execution can occur.
9. Confirm Rocketcart docs explain which context comes from live Ads reads, product intelligence, optimization memory, or user-provided exports.
10. Review changed outputs with the relevant `evals/` prompt before opening a PR.
11. Run or review at least one relevant stress test from `stress-tests/` when safety gates, BSR claims, negatives, budget cuts, or Rocketcart writes are affected.
12. Confirm concrete eval cases have prompt, expected behavior, and pass/fail rubric with `make eval`.
13. Validate all skills with `quick_validate.py` if available.

## Recommended Commands

Use the Makefile for repo-level checks:

```bash
make check-docs
make check-examples
make list-skills
make validate
make eval
```

`make validate` checks required docs, production skill layout, example packs, YAML metadata, and the Codex `quick_validate.py` script when it is available locally. `make eval` checks concrete eval-case structure and pass/fail rubrics. If the local Codex validator is unavailable, the make target skips that step and still runs the structural checks.

GitHub Actions runs the same repo-level checks on pull requests and pushes to `main` through `.github/workflows/validate.yml`.

Manual validator commands are still useful when iterating on one skill:

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
2. Run the example prompt against the changed skill instructions using the relevant files under `sample-data/`.
3. Compare the output with `expected-output-outline.md` and `expected-output.md`.
4. Confirm the output avoids the failure mode in `known-bad-output.md`.
5. Paste the output into relevant eval prompts:
   - `evals/safety-gate-check.md` for any execution recommendation.
   - `evals/bsr-causality-check.md` for BSR, rank, or organic-growth claims.
   - `evals/action-specificity-check.md` for proposed action rows.
   - `evals/missing-data-confidence-check.md` for partial data.
   - `evals/rocketcart-write-gate-check.md` for Rocketcart MCP write candidates.
6. Run or inspect the nearest concrete case under `evals/cases/`.
7. Fix the skill or docs when an eval returns `Needs revision` or `Fail`.

## Stress-Test Review

Use stress tests when changing skill instructions, adding a skill, or reviewing whether the docs are clear for new users:

1. Pick a stress test from `stress-tests/`.
2. Run its prompt against the relevant skill or docs.
3. Confirm the output shows the expected resistance behavior.
4. Paste the output into the listed eval prompts.
5. Strengthen the skill or docs if the output overstates confidence, recommends unsafe execution, cuts strategic traffic, or fails to explain missing data.

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
