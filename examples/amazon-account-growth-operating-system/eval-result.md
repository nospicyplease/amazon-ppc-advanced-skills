# Eval Result

## Review Prompts

- `evals/safety-gate-check.md`: Pass when budget changes and negatives are gated.
- `evals/action-specificity-check.md`: Pass when the queue contains entity IDs, class, action, risk, and gate.
- `evals/missing-data-confidence-check.md`: Pass when competitor, margin, rank, and leakage gaps are visible.
- `evals/bsr-causality-check.md`: Pass when BSR does not override inventory or causality limits.

## Expected Verdict

The expected output should pass. The known-bad output should fail safety and action-specificity checks.
