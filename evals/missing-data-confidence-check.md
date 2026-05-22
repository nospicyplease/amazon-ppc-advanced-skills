# Missing Data Confidence Check

Use this review prompt to make sure an output does not overstate conclusions from partial data.

```text
Review the skill output below for missing-data and confidence handling.

Check whether the output:
1. Lists missing data that could materially change the recommendation.
2. Lowers confidence when margin, total sales, BSR, inventory, Featured Offer / Buy Box, search terms, placement data, competitor context, or comparison windows are missing.
3. Avoids TACoS, incrementality, organic-growth, or profitability claims when required inputs are unavailable.
4. Uses watchlist, investigate, controlled test, or monitor-only actions when evidence is thin.
5. States what additional data would make the recommendation action-safe.

Return:
- Pass / Needs revision / Fail.
- Any overconfident claim.
- Missing data that should be named.
- Safer confidence language.

Skill output:
```
PASTE OUTPUT HERE
```
```
