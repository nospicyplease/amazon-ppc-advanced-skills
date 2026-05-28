# Expected Output

Mode: `masked_output`

Execution: read-only; no Amazon Ads mutation occurred.

Diagnostics:

| profile | campaign | source_rank | spend | sales | orders | clicks | impressions |
|---|---|---:|---:|---:|---:|---:|---:|
| `PROFILE-000001` | `CAMPAIGN-000002` | 1 | 30.00 | 0.00 | 0 | 31 | 3050 |
| `PROFILE-000001` | `CAMPAIGN-000001` | 2 | 12.34 | 123.40 | 5 | 40 | 4000 |
| `PROFILE-000002` | `CAMPAIGN-000001` | 3 | 6.75 | 67.50 | 3 | 18 | 1900 |

Approval packet:

- Every row has an `ACTION-00000N` id.
- Every row is `APPROVAL_REQUIRED`.
- Entity handles are masked, such as `TARGET-000002`, `ST-000002`, and `CAMPAIGN-000001`.
- Exact metrics are copied from source rows without privacy rounding.
- Preflight and readback are required.
- Execution is `not_in_skill_scope`.

Leak scan: public output passed. Private execution manifest was not included in this output.
