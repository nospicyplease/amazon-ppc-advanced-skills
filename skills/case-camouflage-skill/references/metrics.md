# Metrics Reference

Privacy must never change KPIs.

- Keep source metrics exact, including decimals and zero values.
- Do not round, bucket, jitter, aggregate across unlike source IDs, swap between entities, redact selected rows, or merge rows by masked label.
- Compute groupings, ranks, deltas, thresholds, ACoS/ROAS/TACoS, bid rules, budget rules, negative rules, and harvest rules against raw source IDs.
- After analysis, attach masked handles to already-decided findings and actions.
- If an output table drops rows for presentation, say it is a filtered view and keep action packet metrics exact for every row included.

Validation checklist:

- Source record count and displayed record count match for row-level outputs.
- For every included row, exact metric strings or exact decimal values match source.
- Group totals are produced from raw source IDs, not masked handles.
- Ranking ties are resolved with raw source IDs or deterministic source order, never public names.
