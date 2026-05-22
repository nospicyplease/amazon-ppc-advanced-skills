# Examples

Examples show how each production skill should be used and what a good answer should include.

Each skill example contains:

- `prompt.md`: a realistic anonymized prompt.
- `input-summary.md`: available fields, missing fields, assumptions, and scope.
- `expected-output-outline.md`: sections and safety behavior a good answer should include.
- `sample-data/`: small synthetic CSV or JSON fixtures.
- `expected-output.md`: a concrete good-answer target for the fixture.
- `known-bad-output.md`: an unsafe or low-quality answer that should fail review.
- `eval-result.md`: which eval prompts should pass or fail.

These are synthetic teaching and regression fixtures. They are structurally checked by `make check-examples`, but they are not model-scored automated tests.

The Rocketcart example is intentionally richer than a basic optimization review. It demonstrates `Product-Aware Growth Review` mode, including Grow, Fix Before Scaling, Protect, Monitor, and Blocked classifications for low inventory, BSR confounders, weak reviews/rating, competitor price pressure, and unavailable product context.

## How To Use

1. Choose the folder matching the skill you are changing.
2. Paste `prompt.md` into Codex or Claude with `input-summary.md` and the relevant files in `sample-data/`.
3. Compare the output with `expected-output-outline.md` and `expected-output.md`.
4. Confirm it avoids the failure modes in `known-bad-output.md`.
5. Run relevant review prompts from `evals/` and concrete cases from `evals/cases/`.
6. Try at least one relevant adversarial prompt from `stress-tests/` when safety gates are affected.

## Required Fixture Shape

Every production skill should keep this shape:

```text
prompt.md
input-summary.md
expected-output-outline.md
sample-data/
expected-output.md
known-bad-output.md
eval-result.md
```

Run:

```bash
make check-examples
```

Any sample data must be synthetic or anonymized. Do not commit real Amazon or Rocketcart data.
