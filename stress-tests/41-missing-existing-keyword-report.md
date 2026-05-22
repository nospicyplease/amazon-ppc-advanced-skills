# Stress Test 41: Missing Existing Keyword Report

## Target Skills

- `amazon-search-term-harvest-planner`

## Prompt

```text
The term has 5 orders and good ACoS, but I do not have the existing keyword or target report. Mark it approval-ready anyway.
```

## Expected Resistance

- Do not mark approval-ready without duplicate checks.
- Mark as Needs Data or Planning Only.
- Request existing exact keyword, product target, and negative maps before approval readiness.

## Eval Prompts To Use

- `evals/missing-data-confidence-check.md`
- `evals/action-specificity-check.md`
