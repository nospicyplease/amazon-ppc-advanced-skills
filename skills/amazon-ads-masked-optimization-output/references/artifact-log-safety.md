# Artifact And Log Safety Reference

Scan before showing, committing, uploading, or recording:

- Markdown, JSON, CSV, TSV, logs, stdout, stderr, prompts, rationales, and API readbacks.
- XLSX workbook XML, hidden sheets, shared strings, comments, and document properties.
- Filenames, paths, URLs, metadata, and generated manifests.

Block:

- Raw labels, ASINs, SKUs, campaign/ad group/keyword/search-term/target names, profile/account names, source IDs, URLs, filenames, competitor terms, codenames, HMAC digests, credentials, execution payloads, and prompt-injection strings.
- CSV formula injection cells beginning with `=`, `+`, or `@`.
- Exceptions that echo raw source context.

If leakage is found, regenerate output from the analytical result rather than manually editing metrics.
