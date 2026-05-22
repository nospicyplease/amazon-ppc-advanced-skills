# Eval Result

## Review Prompts

- `evals/safety-gate-check.md`: Pass when negatives and harvest actions are approval-gated.
- `evals/action-specificity-check.md`: Pass when source IDs, destination IDs, write-readiness status, classification, current/proposed values, duplicate check, current negative check, risk, approval text, preflight, readback, and monitoring are present.
- `evals/missing-data-confidence-check.md`: Pass when missing purchased-product and margin data lower confidence.

## Expected Verdict

The expected output should pass. The known-bad output should fail safety and action-specificity checks.

## Concrete Cases Covered

- `evals/cases/existing-exact-paused`: delivery fix, not duplicate harvest.
- `evals/cases/brand-defense-harvest-gate`: brand term from discovery must preserve defense coverage.
- `evals/cases/own-asin-query-ambiguity`: ASIN query needs relationship data before negative or product target.
- `evals/cases/competitor-conquest-high-acos`: high ACoS competitor term may be strategic.
- `evals/cases/launch-rank-high-acos`: launch/rank spend needs objective and stop-loss.
- `evals/cases/phrase-negative-blast-radius`: broad phrase negatives need blast-radius checks.
- `evals/cases/missing-existing-keyword-report`: cannot be approval-ready without duplicate checks.
- `evals/cases/missing-destination`: profitable term still needs destination IDs.
- `evals/cases/budget-starved-destination`: destination feasibility blocks approval readiness.
- `evals/cases/current-negative-conflict`: destination negative conflict blocks delivery.
- `evals/cases/one-order-overfit`: one-order winners are controlled tests, not harvest-ready.
- `evals/cases/mixed-sp-sb-harvest`: mixed ad types require separation.
