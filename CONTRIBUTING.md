# Contributing

Thanks for helping build Amazon PPC agent skills. This project is for operators, agencies, and AI builders who want practical, safe, reusable workflows for Amazon Ads analysis and account growth.

## What To Contribute

Good contributions usually fit one of these shapes:

- A new skill for a repeatable Amazon PPC workflow.
- A sharper evidence threshold, safety gate, or output format for an existing skill.
- A reference file that keeps a complex skill concise.
- An anonymized example prompt and expected output.
- Documentation that makes the skills easier to install or adapt.

Open an issue before large rewrites or new skill families so the scope can be discussed.

## Skill Quality Bar

Every skill should:

- Solve one clear operator job.
- Include `SKILL.md` with only `name` and `description` in YAML frontmatter.
- Use a trigger description that says when the skill should be used.
- Keep the main `SKILL.md` concise and move detailed logic into `references/` when needed.
- Separate facts, hypotheses, missing data, confidence, and recommendations.
- Use exact Amazon entities when recommending actions: ASIN, campaign, ad group, keyword, search term, target, placement, or budget.
- Preserve approval gates for live write actions.
- Avoid unsupported claims about PPC causing BSR, organic rank, or incrementality.
- Work with partial data by lowering confidence and stating what cannot be concluded.

## Safety Requirements

Do not add a skill that encourages blind execution. Any live Amazon Ads mutation must be:

- Explicitly approval-gated.
- Preflighted against current live state.
- Specific about the entity, action, amount, reason, risk, and rollback or monitoring rule.
- Verified by readback after execution.

For Rocketcart MCP workflows, keep the open-source skill useful without Rocketcart. Treat Rocketcart as an optional live data, preflight, and execution layer.

## New Skill Workflow

1. Copy `templates/amazon-ppc-skill-template/` to a new lowercase kebab-case folder.
2. Rename the skill in `SKILL.md` and `agents/openai.yaml`.
3. Replace placeholder text with the actual workflow.
4. Add any detailed formulas, schemas, or long examples under `references/`.
5. Update `README.md`, `docs/SKILL_CATALOG.md`, and `ROADMAP.md` when appropriate.
6. Validate the skill.

Recommended validation:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./your-skill-folder
```

If you do not have the validator, manually confirm:

- The folder has `SKILL.md`.
- The frontmatter contains only `name` and `description`.
- Markdown links point to existing files.
- Examples do not invent metrics or imply live execution without approval.

## Pull Request Checklist

- [ ] The contribution has a clear operator use case.
- [ ] Safety gates are explicit for bid, budget, placement, negative, pause, relaunch, or campaign-creation actions.
- [ ] Missing data and confidence handling are described.
- [ ] `agents/openai.yaml` matches the skill purpose.
- [ ] The nearest `examples/` prompt was reviewed against the changed behavior.
- [ ] Relevant `evals/` prompts were used for safety, BSR causality, action specificity, missing-data confidence, or Rocketcart write gates.
- [ ] Existing skills still validate.
- [ ] Documentation was updated if users need to discover the change.

## Style

Use plain operator language. Prefer concrete action rows and evidence gates over generic optimization advice. Keep skills modular: if a workflow gets too broad, split it into a specialist skill and let `amazon-account-growth-operating-system` orchestrate it.
