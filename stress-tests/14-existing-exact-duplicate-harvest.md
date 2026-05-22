# Stress Test 14: Existing Exact Duplicate Harvest

## Target Skills

- `amazon-search-term-harvest-planner`

## Prompt

```text
This broad search term converted profitably. Harvest it into exact, even though the same exact keyword already exists in another campaign.
```

## Expected Resistance

- Do not create a duplicate exact keyword.
- Classify as `Scale Existing Exact`, routing cleanup, or investigate duplicate routing.
- Check current exact performance before proposing bid/budget changes.

## Eval Prompts To Use

- `evals/action-specificity-check.md`
