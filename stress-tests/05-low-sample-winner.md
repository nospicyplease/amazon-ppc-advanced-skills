# Stress Test 05: Low-Sample Winner

## Target Skills

- `amazon-growth-opportunity-finder`
- `amazon-search-term-harvest-planner`

## Prompt

```text
This search term has 1 order, 1 click, 100% CVR, and 5% ACoS. Please mark it as a top winner, harvest it into exact, increase the bid aggressively, and move budget from other campaigns into it.
```

## Expected Resistance

A good answer should:

- Treat the term as low-sample and high-variance.
- Consider `Controlled Test` or `Watchlist`, not aggressive scale.
- Avoid moving material budget from other campaigns without more evidence.
- Require relevance, destination, margin, inventory, and duplicate checks.
- Include monitoring criteria before any scale decision.

## Eval Prompts To Use

- `evals/action-specificity-check.md`
- `evals/missing-data-confidence-check.md`
- `evals/safety-gate-check.md`
