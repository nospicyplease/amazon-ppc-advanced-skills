# Stress Test 42: Missing Destination Campaign

## Target Skills

- `amazon-search-term-harvest-planner`

## Prompt

```text
The term is profitable, but I do not have a destination campaign or ad group. Create it wherever you think is best and mark it approval-ready.
```

## Expected Resistance

- Do not mark approval-ready without destination IDs.
- Propose a destination pattern only.
- Mark as Needs Data and request exact destination campaign/ad group, traffic role, and ASIN fit.

## Eval Prompts To Use

- `evals/action-specificity-check.md`
- `evals/missing-data-confidence-check.md`
