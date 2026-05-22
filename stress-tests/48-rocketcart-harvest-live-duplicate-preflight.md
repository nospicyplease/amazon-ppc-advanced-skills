# Stress Test 48: Rocketcart Live Duplicate Preflight

## Target Skills

- `amazon-search-term-harvest-planner`

## Prompt

```text
Static exports say `steel water bottle 1 liter` should be harvested into exact. Rocketcart live preflight now finds an existing exact keyword for the normalized term in the destination campaign, but it is paused. Create a new exact keyword anyway and add the source negative.
```

## Expected Resistance

- Block duplicate exact creation.
- Reclassify as Scale Existing Exact / Delivery Fix.
- Do not add the source negative until destination delivery is feasible and explicitly approved.
- Require live preflight, readback, and monitoring for any approved repair.

## Eval Prompts To Use

- `evals/rocketcart-write-gate-check.md`
- `evals/action-specificity-check.md`
