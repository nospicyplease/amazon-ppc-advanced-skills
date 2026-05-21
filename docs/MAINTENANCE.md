# Maintenance And Update Guide

## Editing Principles

- Keep each skill self-contained.
- Keep `SKILL.md` concise enough to load into context.
- Put detailed references in a `references/` directory only when needed.
- Do not duplicate large bodies of logic across skills unless the duplication is intentionally local and useful.
- Preserve approval gates for live write actions.
- Keep Amazon terminology current. Use `Featured Offer / Buy Box` when referring to offer ownership.

## Validation Checklist

Before committing updates:

1. Confirm every skill folder has `SKILL.md`.
2. Confirm every `SKILL.md` has valid frontmatter with only `name` and `description`.
3. Confirm `agents/openai.yaml` matches the skill name and purpose.
4. Confirm examples do not invent metrics or imply unsupported live execution.
5. Confirm the Growth Operating System still references both upstream skills correctly.
6. Validate all skills with `quick_validate.py` if available.

## Recommended Commands

```bash
find . -maxdepth 2 -name SKILL.md -print | sort
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./amazon-ads-performance-drop-diagnosis
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./amazon-growth-opportunity-finder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./amazon-account-growth-operating-system
```

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

