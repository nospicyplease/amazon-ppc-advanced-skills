# Eval Result

## Review Prompts

- `evals/safety-gate-check.md`: Pass when scale is approval-gated and inventory-aware.
- `evals/bsr-causality-check.md`: Pass when BSR improvement is a signal, not proof.
- `evals/action-specificity-check.md`: Pass when rows name ASINs, campaign IDs, and search terms.
- `evals/missing-data-confidence-check.md`: Pass when missing margin and blended SB data lower confidence.

## Expected Verdict

The expected output should pass. The known-bad output should fail safety, BSR causality, and missing-data confidence checks.
