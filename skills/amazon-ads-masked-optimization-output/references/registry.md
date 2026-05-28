# Registry Reference

Use a tenant-scoped registry provider instead of bundled CSV mappings.

Provider capabilities:

- Lookup existing handles by raw source ID or text-only identifier.
- Create stable tenant/profile-scoped handles when needed.
- Detect collisions where one source resolves to multiple handles or one handle resolves to multiple sources.
- Block unsafe aliases that preserve customer/project/product/campaign meaning.
- Create placeholders for missing identifiers without inventing source data.
- Reserve planned handles for creation workflows.
- Activate planned handles only after execution readback returns real IDs.
- Transition statuses such as `active`, `placeholder`, `planned`, `retired`, and `blocked`.
- Produce coverage summaries with counts only.

For text-only identifiers, use HMAC-SHA256 with a per-tenant secret. Never expose HMAC digests in packets, logs, coverage, errors, docs, or eval output.

Public repos may include only synthetic registries. Real registries, mappings, source IDs, execution manifests, and raw reports belong in ignored private paths.
