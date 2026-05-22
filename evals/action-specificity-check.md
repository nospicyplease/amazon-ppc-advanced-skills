# Action Specificity Check

Use this review prompt when a skill recommends Amazon PPC actions.

```text
Review the skill output below for action specificity.

Check whether every recommended action includes:
1. Entity type: ASIN, campaign, ad group, keyword, search term, product target, placement, budget, or listing issue.
2. Entity name and exact entity ID when available.
3. Current state or current metric baseline.
4. Proposed action and direction.
5. Reason tied to evidence, not generic optimization language.
6. Expected impact.
7. Risk and confidence.
8. Timing and monitoring window.
9. Approval status for write actions.

Flag:
- Vague actions such as "optimize bids" or "reduce waste" without entity and evidence.
- Exact budget or bid amounts that are unsupported by current values.
- Negatives, pauses, or budget cuts without waste thresholds and strategic-role checks.

Return:
- Pass / Needs revision / Fail.
- Missing fields by action row.
- Revised action-row format.

Skill output:
```
PASTE OUTPUT HERE
```
```
