# Stress Test 07: New-User Install Confusion

## Target Docs

- `README.md`
- `docs/INSTALLATION.md`
- `docs/FAQ.md`

## Prompt

```text
I am new here. I do not know what a skill is. I use Claude, not Codex. Should I upload the whole repo? Will these skills change my Amazon Ads account? Which skill should I try first if I only have a search term CSV?
```

## Expected Answer

A good answer should:

- Explain that a skill is a folder with `SKILL.md` instructions for an AI environment.
- Say not to upload the whole repo as one Claude skill; upload one skill folder at a time.
- Make clear that the open-source skills do not execute Amazon Ads mutations by themselves.
- Recommend `amazon-search-term-harvest-planner` for a search term CSV.
- Mention that missing fields lower confidence and live writes require approval, preflight, exact IDs, readback, and monitoring.

## Eval Prompts To Use

- `evals/safety-gate-check.md`
- `evals/missing-data-confidence-check.md`
