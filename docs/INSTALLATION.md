# Installation

Read [FAQ](FAQ.md) first if you are new to Codex skills, Claude skills, or Rocketcart MCP.

## Requirements

- Codex with local skills support, or Claude with skill upload support.
- This repository cloned locally.
- Optional: Amazon Ads, Business Reports, BSR, inventory, and retail-readiness exports.
- Optional: Rocketcart MCP for live Amazon Ads reads, product intelligence, recent-change context, preflight, approval-gated writes, and readback.

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

For the Rocketcart bridge only:

```bash
mkdir -p ~/.codex/skills
cp -R rocketcart-amazon-ads-live-review ~/.codex/skills/
```

For the case camouflage skill:

```bash
mkdir -p ~/.codex/skills
cp -R skills/case-camouflage-skill ~/.codex/skills/
```

## Install All Skills In Codex

```bash
mkdir -p ~/.codex/skills
cp -R amazon-ads-performance-drop-diagnosis ~/.codex/skills/
cp -R amazon-growth-opportunity-finder ~/.codex/skills/
cp -R amazon-account-growth-operating-system ~/.codex/skills/
cp -R amazon-search-term-harvest-planner ~/.codex/skills/
cp -R rocketcart-amazon-ads-live-review ~/.codex/skills/
cp -R skills/case-camouflage-skill ~/.codex/skills/
```

Reload Codex after copying.

## Install One Skill In Claude

Claude skills are uploaded as skill folders. Zip one skill folder at a time:

```bash
zip -r amazon-account-growth-operating-system.zip amazon-account-growth-operating-system
```

Upload that ZIP in Claude's skill settings.

For the Rocketcart bridge only:

```bash
zip -r rocketcart-amazon-ads-live-review.zip rocketcart-amazon-ads-live-review
```

For the case camouflage skill:

```bash
(cd skills && zip -r ../case-camouflage-skill.zip case-camouflage-skill)
```

Do not upload the entire repository as one Claude skill. Each skill folder is intended to be installed separately.

Include:

- `SKILL.md`.
- `agents/openai.yaml` if useful.
- Any `references/`, `scripts/`, or `assets/` folders used by that skill.

## Verify Installation

In Codex or Claude, start a new chat and invoke the skill by name, for example:

```text
Use $amazon-account-growth-operating-system to build a weekly Amazon PPC action plan from this account data.
```

Installing these open-source skills is separate from connecting Rocketcart MCP. If Rocketcart MCP is available in your host environment, the Rocketcart-aware skill can use it for live Ads + product-intelligence reads. If it is not available, the same skill should run in standalone mode and ask for static exports or pasted product context.

To smoke-test the Rocketcart bridge after install:

```text
Use $rocketcart-amazon-ads-live-review in Live Optimization Review mode. I do not have Rocketcart MCP connected yet. Run in standalone mode and tell me the exact Amazon Ads and product data you need for a safe first review. Do not execute anything.
```

Expected first output:

```text
Mode: Standalone
Review mode: Live Optimization Review
Execution: no writes; approval required for any future live action
Missing data: campaign metrics, search terms, product/ASIN context, inventory, offer status, margin, BSR/category movement, competitor signals, and recent changes
Next step: provide exports or connect Rocketcart MCP for live reads
```

To smoke-test the case camouflage skill after install:

```text
Use $case-camouflage-skill with synthetic Amazon Ads optimization data. Preserve exact KPIs, mask all display labels and identifiers, produce approval packets only, and do not execute Amazon Ads changes.
```

Expected first output:

```text
Mode: masked_output
Execution: read-only; no Amazon Ads mutation
Output: masked diagnostics, approval packet rows, registry coverage summary, and leak-scan result
Gate: separate approved execution tool required for any future writes
```

If you have the Codex skill validator available, run:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-ads-performance-drop-diagnosis
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-growth-opportunity-finder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-account-growth-operating-system
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/amazon-search-term-harvest-planner
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/rocketcart-amazon-ads-live-review
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/case-camouflage-skill
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
cp -R skills/case-camouflage-skill ~/.codex/skills/
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
Use $amazon-search-term-harvest-planner in Live Harvest Review mode for profile example_de. Resolve live campaign/ad group/keyword/negative IDs, check duplicate exacts, current negatives, destination feasibility, product-ad ASIN/SKU context, recent drift, and product readiness. Produce approval-gated harvest rows only. Do not execute anything.
```

```text
Use $rocketcart-amazon-ads-live-review to inspect live Sponsored Products campaign state and product intelligence with Rocketcart MCP, detect recent changes, and propose approval-gated optimization actions without executing writes.
```

For a product-aware Rocketcart review:

```text
Use $rocketcart-amazon-ads-live-review for profile example_de. Confirm the profile, inspect live campaigns and product ads, map campaigns to ASIN context, check category/BSR movement, product readiness, inventory or availability blockers, Featured Offer / Buy Box risk, competitor signals, snapshots, and live drift. Produce proposed action rows only; do not execute writes.
```

### Rocketcart Review Mode Prompts

Live Optimization Review:

```text
Use $rocketcart-amazon-ads-live-review in Live Optimization Review mode for profile example_de. Confirm the profile, inspect live Sponsored Products campaigns, product ads/ASIN mapping, budget and targeting drift, snapshots/changelogs, product readiness, category/BSR movement, and competitor signals. Produce proposed action rows only. Do not execute anything.
```

Product-Aware Growth Review:

```text
Use $rocketcart-amazon-ads-live-review in Product-Aware Growth Review mode for profile example_de. Classify each ASIN/campaign as Grow, Fix Before Scaling, Protect, Monitor, or Blocked using Ads performance plus inventory, Featured Offer / Buy Box, price, reviews/rating, estimated demand, category/BSR movement, competitor signals, margin, and recent changes. Do not execute anything.
```

Preflight / Approval Readiness Review:

```text
Use $rocketcart-amazon-ads-live-review in Preflight / Approval Readiness Review mode for profile example_de. Review these candidate action rows for exact entity IDs, current values, proposed values, product-readiness gates, expected impact, risk, approval text, readback, and monitoring. Mark each row Approval Ready, Needs IDs, Needs Current Value, Needs Product Context, Stale Approval, Blocked, or Monitor Only. Do not execute anything.
```

Post-Change Readback / Monitoring Review:

```text
Use $rocketcart-amazon-ads-live-review in Post-Change Readback / Monitoring Review mode for profile example_de. Review the approved changes from the last execution window, read back affected entities, compare expected versus current state, and classify each action as Readback Confirmed, Partially Applied, Not Applied, Monitoring, Worked, Failed, or Needs More Data. Do not execute new writes.
```

Search-Term Execute Approved Rows:

```text
Use $amazon-search-term-harvest-planner in Execute Approved Rows mode for profile example_de. Approved rows: H-003 only. Rerun live preflight, confirm exact IDs and current/proposed values, execute only H-003 if the current state still matches, read back the affected entity, and report 3/7/14-day monitoring. Do not execute any other row.
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

- Install one of the skill folders, not `docs/`, `examples/`, `evals/`, or `templates/` unless you are creating a new skill.

Examples and evals do not trigger as skills:

- `examples/`, `evals/`, and `stress-tests/` are teaching and review materials. They are not installed as runtime skills.

Rocketcart MCP unavailable:

- Use standalone mode with static exports or pasted data.
- The Rocketcart-aware skill should lower confidence when live Ads reads, product-intelligence reads, preflight, or readback are unavailable.

## Data Handling

The skills can work with partial data, but they must state confidence limits. Missing margin, total sales, BSR, inventory, Featured Offer / Buy Box, search terms, or comparison windows should lower confidence and block unsafe recommendations.

See [Data privacy](DATA_PRIVACY.md) before adding examples or sharing account data.
