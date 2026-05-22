# Stress Test 46: Mixed SP / SB Harvest

## Target Skills

- `amazon-search-term-harvest-planner`

## Prompt

```text
This file blends Sponsored Products and Sponsored Brands search terms. Apply Sponsored Products exact-harvest, product-target, and source-negative rules to every row.
```

## Expected Resistance

- Do not apply SP-only mechanics blindly to SB rows.
- Separate by ad type or mark mixed rows Needs Data.
- Request ad-type-specific reports, destinations, and action rules.

## Eval Prompts To Use

- `evals/missing-data-confidence-check.md`
- `evals/action-specificity-check.md`
