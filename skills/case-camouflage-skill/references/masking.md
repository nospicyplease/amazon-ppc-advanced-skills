# Masking Reference

Mask only the display plane. Do not alter analytical data, source reports, exact metrics, grouping keys, ranking keys, or attribution keys.

Mask these user-facing values whenever output may be public, demoed, recorded, logged, or committed:

- Account, profile, tenant, project, customer, and codename labels.
- Product names, ASINs, SKUs, parent/child identifiers, and listing URLs.
- Campaigns, ad groups, portfolios, keywords, search terms, product targets, category targets, and placements.
- Filenames, file paths, worksheet names, URLs, request IDs, source IDs, and any source-derived identifiers.

Use stable handles:

- Tenant/account/profile: `ACCOUNT-000001`, `PROFILE-000001`.
- Product and catalog: `PRODUCT-000001`, `ASIN-000001`, `SKU-000001`.
- Ads entities: `CAMPAIGN-000001`, `ADGROUP-000001`, `KW-000001`, `ST-000001`, `TARGET-000001`, `PLACEMENT-000001`.
- Other source-derived values: `FILE-000001`, `URL-000001`, `ID-000001`.

Handles are tenant/profile scoped. If `CAMPAIGN-000001` appears in more than one profile, always show the masked profile handle next to it.

Do not use cute aliases, customer initials, product descriptors, marketplace hints, category hints, or partially retained ASIN/SKU fragments.
