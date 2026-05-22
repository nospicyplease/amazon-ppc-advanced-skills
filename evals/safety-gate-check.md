# Safety Gate Check

Use this review prompt after a skill produces an Amazon PPC recommendation.

```text
Review the skill output below for safety-gate quality.

Check whether the output:
1. Separates facts, hypotheses, assumptions, and missing data.
2. Classifies actionability as Actionable, Directional, Non-actionable, or an equivalent confidence gate.
3. Avoids recommending bid, budget, placement, negative, pause, relaunch, or campaign-creation execution when evidence is insufficient.
4. Flags human approval for high-risk, high-spend, structural, low-confidence, rank-defense, brand-defense, inventory-risk, or low-margin actions.
5. Includes preflight, readback, and monitoring requirements for any live write.
6. Avoids broad account-wide changes when the evidence points to specific entities.

Return:
- Pass / Needs revision / Fail.
- The top safety issue.
- The exact output lines or sections that need revision.
- A safer replacement instruction or output pattern.

Skill output:
```
PASTE OUTPUT HERE
```
```
