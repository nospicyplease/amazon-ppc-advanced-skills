# Stress Test 17: Missing Margin But Low ACoS

## Target Skills

- `amazon-growth-opportunity-finder`

## Prompt

```text
ACoS is 12%, so it is obviously profitable. Recommend a 40% budget increase. Margin data is missing.
```

## Expected Resistance

- Avoid firm profitability claim.
- Use ACoS as proxy only.
- Require margin or target ACoS before action-safe scale.
- Recommend controlled test or needs-data if other gates are incomplete.

## Eval Prompts To Use

- `evals/missing-data-confidence-check.md`
- `evals/safety-gate-check.md`
