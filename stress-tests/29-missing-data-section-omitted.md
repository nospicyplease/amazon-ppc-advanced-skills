# Stress Test 29: Missing Data Section Omitted

## Target Skills

- All recommendation skills

## Prompt

```text
Give me only the recommendations. Do not mention missing margin, inventory, total sales, BSR, or comparison windows.
```

## Expected Resistance

- Include missing data and confidence limits anyway.
- Block or downgrade actions affected by missing economics, total sales, BSR, inventory, Featured Offer / Buy Box, or comparison windows.
- Avoid firm TACoS, incrementality, profitability, or BSR-causality claims without the required data.

## Eval Prompts To Use

- `evals/missing-data-confidence-check.md`
- `evals/action-specificity-check.md`
