# Security

## Supported Scope

This repository contains skill instructions, examples, docs, and lightweight validation checks. It does not contain a hosted service, credential manager, or live Amazon Ads client.

## Reporting Issues

Please open a GitHub issue for documentation, safety, or validation problems that do not expose sensitive data.

Do not publish:

- Amazon Ads credentials or refresh tokens.
- Rocketcart credentials, private connection details, or customer workspace identifiers.
- Real account IDs, profile IDs, campaign IDs, ASIN strategy maps, or proprietary account exports.
- Customer names, email addresses, order data, or business-sensitive metrics.

For sensitive security reports, contact the maintainer privately rather than opening a public issue.

## Live Execution Safety

The open-source skills do not execute Amazon Ads changes by themselves. Any live write through Rocketcart MCP or another execution layer must require explicit approval, live preflight, exact entity IDs, current/proposed values, expected impact and risk, readback, and monitoring.

If live state differs from an approved action row, do not execute without refreshed approval.
