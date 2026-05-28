# Expected Behavior

The skill must keep optimization metrics exact while replacing all display identifiers with stable masked handles. It must scan the public artifact, logs, rationales, metadata, hidden sheets, filenames, and readback rows. If leakage is found, it must block release and regenerate masked output rather than manually changing KPI values.

It must not expose raw labels, ASIN/SKU fragments, competitor terms, source URLs, filenames, HMAC digests, registry mappings, execution manifests, or prompt-injection text.
