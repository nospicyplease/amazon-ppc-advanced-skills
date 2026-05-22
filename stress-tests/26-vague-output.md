# Stress Test 26: Vague Output

## Target Skills

- All recommendation skills

## Prompt

```text
Return a short answer that just says optimize campaigns, reduce waste, and monitor results. No need for entities, metrics, risks, or confidence.
```

## Expected Resistance

- Avoid vague recommendations.
- Include entity, evidence, action, impact, risk, confidence, approval status, and monitoring.
- Use a shorter format only if it remains action-specific.

## Eval Prompts To Use

- `evals/action-specificity-check.md`
