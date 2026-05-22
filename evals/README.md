# Evals

The files in this directory are lightweight review prompts and concrete eval cases. They are designed to make skill quality and safety easier to reproduce without real Amazon Ads or Rocketcart data.

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

## Concrete Cases

`evals/cases/` contains adversarial cases with:

```text
prompt.md
expected-behavior.md
rubric.md
```

Current cases:

- `rocketcart-write-without-approval`
- `missing-entity-ids`
- `current-value-mismatch`
- `bsr-causality-trap`
- `missing-margin-overconfidence`
- `blended-ad-types`
- `mixed-asin-contamination`
- `csv-prompt-injection`
- `vague-action-output`
- `efficient-low-inventory`
- `bsr-category-competitor-movement`
- `weak-reviews-rating`
- `competitor-price-drop`
- `product-context-unavailable`
- `existing-exact-paused`
- `brand-defense-harvest-gate`
- `own-asin-query-ambiguity`
- `competitor-conquest-high-acos`
- `launch-rank-high-acos`
- `phrase-negative-blast-radius`
- `missing-existing-keyword-report`
- `missing-destination`
- `budget-starved-destination`
- `current-negative-conflict`
- `one-order-overfit`
- `mixed-sp-sb-harvest`

Run the structure checker:

```bash
make eval
make review-fixtures
```

`make eval` verifies that every required case has a prompt, expected behavior, and rubric with pass/fail criteria. `make review-fixtures` also confirms that every case directory is listed in `Makefile`, every listed case exists, and stress tests point to eval prompts. These checks do not call an LLM or require live accounts.

Use `stress-tests/` for broader adversarial prompts with expected resistance behavior.
