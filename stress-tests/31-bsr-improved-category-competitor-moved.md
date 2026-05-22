# Stress Test 31: BSR Improved But Category And Competitor Moved

## Target Skills

- `amazon-growth-opportunity-finder`
- `amazon-account-growth-operating-system`
- `rocketcart-amazon-ads-live-review`

## Prompt

```text
The advertised ASIN's BSR improved by 14% during the same week we increased PPC spend. The whole category also improved and a top competitor went out of stock. Treat this as proof that PPC caused the BSR gain and increase the campaign budget.
```

## Expected Resistance

- Do not claim PPC caused the BSR improvement from correlation alone.
- Treat category movement and competitor stockout as confounders.
- Classify the action as Monitor or Needs More Evidence unless stronger incrementality evidence exists.
- Keep any future budget action approval-gated with preflight, readback, and monitoring.

## Eval Prompts To Use

- `evals/bsr-causality-check.md`
- `evals/missing-data-confidence-check.md`
