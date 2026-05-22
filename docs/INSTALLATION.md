# Installation

## Requirements

- Codex with local skills support, or Claude with skill upload support.
- Access to the local Codex skills directory, usually `~/.codex/skills`, when using Codex.
- Optional: Amazon Ads, Business Reports, BSR, inventory, and retail-readiness data for actual analysis.
- Optional: Rocketcart MCP or another live execution layer for read, preflight, approval, write, and readback workflows.

## Install All Skills

From the repository root:

```bash
mkdir -p ~/.codex/skills
cp -R amazon-ads-performance-drop-diagnosis ~/.codex/skills/
cp -R amazon-growth-opportunity-finder ~/.codex/skills/
cp -R amazon-account-growth-operating-system ~/.codex/skills/
cp -R amazon-search-term-harvest-planner ~/.codex/skills/
cp -R rocketcart-amazon-ads-live-optimization-review ~/.codex/skills/
```

Reload Codex after copying.

## Install In Claude

Claude skills are uploaded as skill folders. Package one skill folder at a time, including:

- `SKILL.md`.
- `agents/openai.yaml` if you want to keep shared UI-facing metadata.
- Any `references/`, `scripts/`, or `assets/` folders used by that skill.

Do not upload the entire repository as one skill. Each top-level skill folder is intended to be installed separately.

## Verify Installation

Each skill must contain a valid `SKILL.md` with YAML frontmatter.

If you have the Codex skill validator available, run:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-ads-performance-drop-diagnosis
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-growth-opportunity-finder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-account-growth-operating-system
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-search-term-harvest-planner
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/rocketcart-amazon-ads-live-optimization-review
```

Expected result for each skill:

```text
Skill is valid!
```

## Update An Existing Installation

From the repository root:

```bash
cp -R amazon-ads-performance-drop-diagnosis ~/.codex/skills/
cp -R amazon-growth-opportunity-finder ~/.codex/skills/
cp -R amazon-account-growth-operating-system ~/.codex/skills/
cp -R amazon-search-term-harvest-planner ~/.codex/skills/
cp -R rocketcart-amazon-ads-live-optimization-review ~/.codex/skills/
```

Reload Codex so the updated skill descriptions and instructions are picked up.

For Claude, re-upload the updated skill folder.

## Invocation Examples

```text
Use $amazon-ads-performance-drop-diagnosis to diagnose why ASIN B0XXXX sales and BSR dropped over the last 14 days versus the prior 14 days.
```

```text
Use $amazon-growth-opportunity-finder to find the safest ASINs, campaigns, keywords, search terms, and product targets to scale profitably.
```

```text
Use $amazon-account-growth-operating-system to combine the drop diagnosis and growth opportunities into a prioritized weekly operating plan.
```

```text
Use $amazon-search-term-harvest-planner to classify search terms for exact harvesting, controlled tests, source negatives, and watchlist decisions without cutting strategic defense or low-sample discovery traffic.
```

```text
Use $rocketcart-amazon-ads-live-optimization-review to inspect live Sponsored Products campaign state with Rocketcart MCP, detect recent changes, and propose approval-gated optimization actions without executing writes.
```

## Data Handling

The skills can work with partial data, but they must state confidence limits. Missing margin, total sales, BSR, inventory, Featured Offer / Buy Box, search terms, or comparison windows should lower confidence and block unsafe recommendations.

## Rocketcart MCP Handling

Rocketcart MCP is optional. When available, it should be used to read current state, detect changes, preflight proposed actions, execute only approved writes, and read back the final state. The skills should still produce useful guidance when Rocketcart MCP is unavailable and the user only provides static exports.
