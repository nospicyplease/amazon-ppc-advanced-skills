# Stress Tests

These prompts are designed to pressure-test the repo's core promises:

- Do not execute or imply live Amazon Ads writes without approval, preflight, exact IDs, readback, and monitoring.
- Do not overstate BSR, TACoS, profitability, or incrementality when data is missing.
- Do not recommend negatives, pauses, budget cuts, or bid reductions from weak evidence.
- Preserve brand defense, own-ASIN defense, launch/rank support, and strategic discovery unless waste is clearly isolated.

## How To Use

1. Pick the stress test closest to the skill you changed.
2. Run the prompt against the skill.
3. Compare the output to the expected resistance behavior in the file.
4. Paste the output into the relevant `evals/` prompt.
5. Revise the skill when it fails or becomes overconfident.

Passing a stress test does not prove a skill is perfect. Failing one is useful: it shows where the instructions need stronger gates.

Run the fixture quality gate after editing stress tests:

```bash
make review-fixtures
```

Each stress test must name target production skills, include a prompt, describe expected resistance, and list eval prompt paths. If a prompt asks for immediate execution, no-approval writes, broad negatives, or another unsafe shortcut, the expected resistance must explicitly block execution or require approval-gated behavior.

## Stress Test Files

- `01-no-data-overconfidence.md`
- `02-bsr-causality-trap.md`
- `03-unsafe-negative-trap.md`
- `04-rocketcart-write-without-approval.md`
- `05-low-sample-winner.md`
- `06-conflicting-upstream-findings.md`
- `07-new-user-install-confusion.md`
- `08-ambiguous-rocketcart-profile.md`
- `09-missing-entity-ids.md`
- `10-current-value-mismatch.md`
- `11-dry-run-passes-inventory-blocked.md`
- `12-approved-row-missing-monitoring.md`
- `13-branded-defense-zero-orders.md`
- `14-existing-exact-duplicate-harvest.md`
- `15-negative-phrase-own-asin-defense.md`
- `16-unstable-buy-box.md`
- `17-missing-margin-low-acos.md`
- `18-missing-total-sales-tacos.md`
- `19-bsr-improves-units-decline.md`
- `20-bsr-category-change.md`
- `21-same-day-data-incomplete.md`
- `22-blended-ad-types.md`
- `23-placement-specific-problem.md`
- `24-mixed-asin-contamination.md`
- `25-csv-prompt-injection.md`
- `26-vague-output.md`
- `27-budget-increase-without-current-budget.md`
- `28-write-capability-available-initial-review.md`
- `29-missing-data-section-omitted.md`
- `30-highly-efficient-low-inventory.md`
- `31-bsr-improved-category-competitor-moved.md`
- `32-weak-reviews-rating-scale-block.md`
- `33-competitor-price-drop-scale-risk.md`
- `34-product-context-unavailable.md`
- `35-existing-exact-paused.md`
- `36-brand-defense-discovery-term.md`
- `37-own-asin-query-ambiguity.md`
- `38-competitor-conquest-high-acos.md`
- `39-launch-rank-high-acos.md`
- `40-phrase-negative-blast-radius.md`
- `41-missing-existing-keyword-report.md`
- `42-missing-destination-campaign.md`
- `43-budget-starved-destination.md`
- `44-current-negative-conflict.md`
- `45-one-order-overfit-harvest.md`
- `46-mixed-sp-sb-harvest.md`
