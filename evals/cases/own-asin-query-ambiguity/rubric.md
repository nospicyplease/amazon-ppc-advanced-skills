# Rubric

## Pass Criteria

- Flags missing ASIN relationship or purchased-product data.
- Blocks source negative until own-ASIN defense risk is resolved.
- Marks the row `NEEDS_DATA` or planning-only.
- Requests ASIN map and destination details.

## Fail Criteria

- Adds product target and source negative without ASIN context.
- Ignores own-ASIN defense risk.
- Marks the action approval-ready.
- Omits missing-data confidence notes.
