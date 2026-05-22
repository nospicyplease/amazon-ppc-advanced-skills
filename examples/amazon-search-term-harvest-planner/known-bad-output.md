# Known Bad Output

```text
Harvest all converting terms into exact campaigns and add source negatives everywhere. Create a duplicate exact for `steel water bottle 1 liter`, negative the ASIN substitute term, add a phrase negative for `water bottle`, scale the one-order `steel bottle` query, and ignore the paused exact keyword, budget-starved destination, current negative conflict, and mixed SB/SP data.
```

## Why This Fails

- Creates duplicate exact keywords.
- Adds source negatives solely because terms were harvested.
- Risks cutting brand defense and own-ASIN defense.
- Uses a broad phrase negative with unsafe blast radius.
- Treats one-order terms as action-ready.
- Ignores existing exact paused, destination budget, and current negative conflicts.
- Applies SP-only logic to mixed SB/SP data.
- Omits write-readiness status, current/proposed values, approval gates, exact destination checks, preflight, readback, and monitoring.
