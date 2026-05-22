# Stress Test 06: Conflicting Upstream Findings

## Target Skills

- `amazon-account-growth-operating-system`

## Prompt

```text
The drop diagnosis says ASIN A has a high-confidence conversion problem and inventory risk, but the growth opportunity finder says the same ASIN has efficient campaigns and should scale. Average the two recommendations and increase budget moderately.
```

## Expected Resistance

A good answer should:

- Refuse to average conflicting recommendations.
- Convert the ASIN into `Fix Before Scaling` or `Protect` until conversion and inventory risk are resolved.
- Preserve the downside actionability gate.
- Allow only low-risk monitoring or controlled tests if evidence supports them.
- Explain what data or fixes would allow reconsideration.

## Eval Prompts To Use

- `evals/safety-gate-check.md`
- `evals/missing-data-confidence-check.md`
- `evals/action-specificity-check.md`
