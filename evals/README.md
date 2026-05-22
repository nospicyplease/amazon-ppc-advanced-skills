# Evals

The files in this directory are review prompts, not automated tests. Use them to inspect whether a skill output preserves the repo's quality and safety bar.

## Current Review Prompts

- `safety-gate-check.md`: live-write safety and approval gates.
- `bsr-causality-check.md`: BSR, rank, and PPC-to-organic discipline.
- `action-specificity-check.md`: whether action rows are specific enough.
- `missing-data-confidence-check.md`: whether partial data lowers confidence.
- `rocketcart-write-gate-check.md`: Rocketcart MCP write safety.

## How To Use

1. Generate an output from a skill using an example or real anonymized prompt.
2. Paste the output into the relevant eval prompt.
3. Treat `Needs revision` or `Fail` as a reason to revise the skill, docs, or example.

## Future Automated Structure

The repo can later add:

```text
evals/cases/
evals/fixtures/
evals/expected/
```

For now, `stress-tests/` contains adversarial prompts with expected resistance behavior.
