# Expected Output Outline

1. Scope and mode: read-only masked optimization output.
2. Data coverage: synthetic records loaded, registry coverage counts only.
3. Diagnostics: campaign/profile masked handles with exact spend, sales, orders, clicks, and impressions.
4. Approval packet: masked action rows for bid, budget, negative, and harvest recommendations.
5. Execution gate: no direct Amazon Ads writes; private manifest is separate and ignored.
6. Readback example: masked status rows only.
7. Leakage scan: public output passed.
8. Production readiness: not claimed unless synthetic tests, leakage tests, and real-profile dry-runs pass.
