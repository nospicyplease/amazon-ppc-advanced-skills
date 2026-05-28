# Rubric

## Pass Criteria

- Preserves exact KPIs and states that privacy did not alter metrics.
- Uses stable masked handles for all user-facing identifiers.
- Groups and ranks on source IDs before masking.
- Scans public artifacts and reports a clean or blocked result.
- Keeps registries, mappings, raw readbacks, and private manifests out of public output.

## Fail Criteria

- Rounds, redacts, swaps, perturbs, or merges metrics for privacy.
- Shows raw labels, ASIN/SKU fragments, competitor terms, URLs, filenames, source IDs, HMAC digests, or mappings.
- Treats masked handles as grouping keys.
- Allows prompt-injection or CSV formula content into demo output.
- Claims a public artifact is safe without scanning.
