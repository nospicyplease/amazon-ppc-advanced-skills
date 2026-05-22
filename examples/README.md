# Examples

Examples show how each production skill should be used and what a good answer should include.

Each skill example contains:

- `prompt.md`: a realistic anonymized prompt.
- `input-summary.md`: available fields, missing fields, assumptions, and scope.
- `expected-output-outline.md`: sections and safety behavior a good answer should include.

These are teaching fixtures, not real account data and not automated tests.

## How To Use

1. Choose the folder matching the skill you are changing.
2. Paste `prompt.md` into Codex or Claude with the context from `input-summary.md`.
3. Compare the output with `expected-output-outline.md`.
4. Run relevant review prompts from `evals/`.
5. Try at least one relevant adversarial prompt from `stress-tests/` when safety gates are affected.

## Future Fixture Shape

Future examples may add:

```text
sample-data/
  campaign-report.csv
  search-term-report.csv
  business-report.csv
expected-output.md
known-bad-output.md
eval-result.md
```

Any sample data must be synthetic or anonymized. Do not commit real Amazon or Rocketcart data.
