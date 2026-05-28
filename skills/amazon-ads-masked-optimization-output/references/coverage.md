# Coverage Reference

Coverage summaries are safe only when they contain counts and statuses, not mappings.

Good:

- `total_handles`
- counts by `entity_type`
- counts by status: `active`, `placeholder`, `planned`, `retired`, `blocked`
- missing coverage categories such as "2 placeholder targets"
- scanner surfaces checked

Bad:

- raw ID to handle mappings
- handle to raw label mappings
- HMAC digests
- source filenames
- customer/profile names
- exact registry URIs or credential names beyond generic env var names

Do not claim production-ready unless synthetic tests, leakage tests, and real-profile dry-runs pass.

For local real-profile validation, create ignored private scaffolding with `make prepare-private-dry-run`, then place the real read-only registry and `profile-<profile_id>.json` fixtures in `PRIVATE_TEST_DATA_DIR`.
