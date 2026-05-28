# Input Summary

Synthetic inputs include:

- Two profile IDs across two marketplaces.
- Sponsored Products campaign, target, search-term, ASIN, and SKU identifiers.
- Exact KPI strings for spend, sales, orders, clicks, impressions, bids, budgets, budget utilization, and target ACoS.
- A synthetic registry with stable handles and unsafe alias examples.

Missing by design:

- Real credentials.
- Real Amazon Ads reports.
- Real registry mappings.
- Live execution adapter.

Expected mode: read-only masked output. No Amazon Ads mutation is allowed.
