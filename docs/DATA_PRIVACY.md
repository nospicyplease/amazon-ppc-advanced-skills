# Data Privacy

This repository should be safe to browse, fork, and contribute to without exposing real Amazon account data.

## Do Not Commit Real Account Data

Do not commit:

- Real Amazon Ads exports.
- Real Business Reports.
- Real BSR or organic-rank exports tied to identifiable products.
- Customer names, account names, profile IDs, advertiser IDs, campaign IDs, ad group IDs, keyword IDs, target IDs, or SKU/FNSKU values.
- Rocketcart customer data, credentials, private connection details, snapshots, changelogs, or proprietary performance data.
- Rocketcart product-intelligence results tied to real products, including BSR/category rank, stock/availability, price, estimated demand, competitor alerts, reviews, rating, or ASIN-level controls.
- Search terms that reveal confidential launch strategy, competitor strategy, or brand-sensitive information.

## Anonymization Rules

Use synthetic or heavily anonymized values:

- ASINs: `ASIN-A`, `B0EXAMPLE1`, `PARENT-ALPHA`.
- Campaigns: `SP-US-EXACT-WINNER`, `SP-DE-AUTO-DISCOVERY`.
- Profiles: `example_us`, `example_de`.
- Search terms: use generic category examples or redacted terms.
- Metrics: change enough that they cannot be tied back to a real account.

## Examples And Stress Tests

Examples, evals, and stress tests must be teaching fixtures, not real account extracts. If a file looks like a CSV export, it must be synthetic and clearly safe to publish.

## Rocketcart MCP

Rocketcart MCP can expose live account state in real deployments. Do not paste or commit live account results unless they are anonymized. Do not include proprietary Rocketcart implementation details unless they are already public and intended for this repo.

## Live Writes

These skills do not execute Amazon Ads changes by themselves. Any live write must remain approval-gated with preflight, exact entity IDs, current/proposed values, readback, and monitoring.
