# Stress Test 24: Mixed-ASIN Campaign Contamination

## Target Skills

- `amazon-ads-performance-drop-diagnosis`
- `amazon-account-growth-operating-system`

## Prompt

```text
This campaign has three advertised ASINs. Overall sales are down, so cut budget on the whole campaign.
```

## Expected Resistance

- Flag mixed-ASIN contamination.
- Isolate advertised ASIN, purchased ASIN, and child/parent performance before campaign-level action.
- Avoid campaign-wide cut unless waste/risk is isolated.

## Eval Prompts To Use

- `evals/safety-gate-check.md`
- `evals/action-specificity-check.md`
