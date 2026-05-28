# Eval Result

The expected output passes when:

- No raw campaign, profile, ASIN, SKU, search-term, filename, URL, or source-derived identifier appears.
- Exact KPIs match the synthetic source fixture.
- Diagnostics are grouped and ranked before masking.
- Approval rows are masked and approval-gated.
- Private execution manifests are absent from public/demo output.
- The answer does not claim production readiness unless real-profile dry-runs pass.
