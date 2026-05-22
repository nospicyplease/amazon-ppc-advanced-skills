# Installation

Read [FAQ](FAQ.md) first if you are new to Codex skills, Claude skills, or Rocketcart MCP.

## Requirements

- Codex with local skills support, or Claude with skill upload support.
- This repository cloned locally.
- Optional: Amazon Ads, Business Reports, BSR, inventory, and retail-readiness exports.
- Optional: Rocketcart MCP for live reads, preflight, approval-gated writes, and readback.

## Clone The Repo

```bash
git clone https://github.com/nospicyplease/amazon-ppc-advanced-skills.git
cd amazon-ppc-advanced-skills
```

## Install One Skill In Codex

Use this when you only want one workflow.

```bash
mkdir -p ~/.codex/skills
cp -R amazon-account-growth-operating-system ~/.codex/skills/
```

Reload Codex so the skills list refreshes.

## Install All Skills In Codex

```bash
mkdir -p ~/.codex/skills
cp -R amazon-ads-performance-drop-diagnosis ~/.codex/skills/
cp -R amazon-growth-opportunity-finder ~/.codex/skills/
cp -R amazon-account-growth-operating-system ~/.codex/skills/
cp -R amazon-search-term-harvest-planner ~/.codex/skills/
cp -R rocketcart-amazon-ads-live-optimization-review ~/.codex/skills/
```

Reload Codex after copying.

## Install One Skill In Claude

Claude skills are uploaded as skill folders. Zip one skill folder at a time:

```bash
zip -r amazon-account-growth-operating-system.zip amazon-account-growth-operating-system
```

Upload that ZIP in Claude's skill settings.

Do not upload the entire repository as one Claude skill. Each top-level skill folder is intended to be installed separately.

Include:

- `SKILL.md`.
- `agents/openai.yaml` if useful.
- Any `references/`, `scripts/`, or `assets/` folders used by that skill.

## Verify Installation

In Codex or Claude, start a new chat and invoke the skill by name, for example:

```text
Use $amazon-account-growth-operating-system to build a weekly Amazon PPC action plan from this account data.
```

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

Manual validation if the Codex validator is unavailable:

- Confirm the installed skill folder contains `SKILL.md`.
- Confirm `SKILL.md` starts with YAML frontmatter containing only `name` and `description`.
- Confirm any linked `references/` files exist.
- Confirm `agents/openai.yaml` exists if the skill includes UI metadata.

## Update An Existing Installation

Copy the updated skill folder again, then reload Codex:

```bash
cp -R amazon-account-growth-operating-system ~/.codex/skills/
```

For Claude, rebuild and re-upload the ZIP for the updated skill folder.

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

## First Smoke Test

After installing one skill, use the matching `examples/<skill-name>/prompt.md` with the context in `input-summary.md`. A good output should follow `expected-output-outline.md`.

## Troubleshooting

Skill does not appear:

- Reload Codex or Claude after installing.
- Confirm the folder is directly under `~/.codex/skills/`, not nested one level deeper.
- Confirm the folder contains `SKILL.md`.

Wrong folder zipped for Claude:

- The ZIP should contain the skill folder and its `SKILL.md`.
- Do not zip the whole repository for a single Claude skill.

Stale copied skill:

- Re-copy the skill folder from the repo and reload the app.

Missing `SKILL.md`:

- Install one of the top-level skill folders, not `docs/`, `examples/`, `evals/`, or `templates/` unless you are creating a new skill.

Examples and evals do not trigger as skills:

- `examples/`, `evals/`, and `stress-tests/` are teaching and review materials. They are not installed as runtime skills.

Rocketcart MCP unavailable:

- Use standalone mode with static exports or pasted data.
- The Rocketcart-aware skill should lower confidence when live reads, preflight, or readback are unavailable.

## Data Handling

The skills can work with partial data, but they must state confidence limits. Missing margin, total sales, BSR, inventory, Featured Offer / Buy Box, search terms, or comparison windows should lower confidence and block unsafe recommendations.

See [Data privacy](DATA_PRIVACY.md) before adding examples or sharing account data.
