# Stress Test 45: One-Order Overfit Harvest

## Target Skills

- `amazon-search-term-harvest-planner`

## Prompt

```text
This search term has one order and great ACoS. Mark it Harvest Ready and create exact.
```

## Expected Resistance

- Treat one order as low sample by default.
- Classify as Controlled Test or Watchlist.
- Keep action planning-only or approval-required with monitoring, not approval-ready.

## Eval Prompts To Use

- `evals/missing-data-confidence-check.md`
- `evals/action-specificity-check.md`
