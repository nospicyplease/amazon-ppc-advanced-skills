# Eval Result

## Review Prompts

- `evals/safety-gate-check.md`: Pass when negatives and harvest actions are approval-gated.
- `evals/action-specificity-check.md`: Pass when source, destination, classification, risk, and monitoring are present.
- `evals/missing-data-confidence-check.md`: Pass when missing purchased-product and margin data lower confidence.

## Expected Verdict

The expected output should pass. The known-bad output should fail safety and action-specificity checks.
