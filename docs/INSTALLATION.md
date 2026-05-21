# Installation

## Requirements

- Codex with local skills support.
- Access to the local Codex skills directory, usually `~/.codex/skills`.
- Optional: Amazon Ads, Business Reports, BSR, inventory, and retail-readiness data for actual analysis.

## Install All Skills

From the repository root:

```bash
mkdir -p ~/.codex/skills
cp -R amazon-ads-performance-drop-diagnosis ~/.codex/skills/
cp -R amazon-growth-opportunity-finder ~/.codex/skills/
cp -R amazon-account-growth-operating-system ~/.codex/skills/
```

Reload Codex after copying.

## Verify Installation

Each skill must contain a valid `SKILL.md` with YAML frontmatter.

If you have the Codex skill validator available, run:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-ads-performance-drop-diagnosis
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-growth-opportunity-finder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-account-growth-operating-system
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
```

Reload Codex so the updated skill descriptions and instructions are picked up.

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

## Data Handling

The skills can work with partial data, but they must state confidence limits. Missing margin, total sales, BSR, inventory, Featured Offer / Buy Box, search terms, or comparison windows should lower confidence and block unsafe recommendations.

