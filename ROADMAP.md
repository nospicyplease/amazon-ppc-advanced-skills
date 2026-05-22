# Roadmap

This roadmap is intentionally practical: every item should help an Amazon operator, agency, or AI builder turn messy account data into safer decisions.

## Project Direction

Amazon PPC Advanced Skills should become an open-source library of expert agent workflows for:

- Diagnosing performance drops and account risks.
- Finding profitable growth opportunities.
- Turning findings into approval-ready action queues.
- Teaching safe live-operation patterns for Rocketcart MCP and other execution layers.

The skills must remain useful with static exports in Codex or Claude. Rocketcart MCP should be additive: live Amazon Ads reads, product intelligence, recent-change context, preflight checks, snapshots, guarded execution, and readback.

## Near-Term Priorities

1. Contributor foundation: templates, issue templates, roadmap, and clearer install docs.
2. Harden the Rocketcart MCP bridge skill with anonymized examples and evaluation prompts.
3. Add sample prompts and expected outputs for each existing skill.
4. Add more specialist PPC skills that plug into the existing operating system.
5. Add validation and evaluation examples that show what good outputs look like.

## Current Maturity

| Skill | Status | Main Gap Before v1 |
|---|---|---|
| `amazon-ads-performance-drop-diagnosis` | Production-oriented draft | More sample data fixtures and known-bad outputs. |
| `amazon-growth-opportunity-finder` | Production-oriented draft | Clearer thresholds for scale vs watchlist decisions by data volume. |
| `amazon-account-growth-operating-system` | Orchestrator draft | More examples showing conflict resolution across upstream findings. |
| `amazon-search-term-harvest-planner` | Good-first-skill complete | Fixture coverage for duplicate exact keywords and source-negative blockers. |
| `rocketcart-amazon-ads-live-optimization-review` | Rocketcart bridge draft | Deeper product-intelligence examples, preflight examples, and post-change monitor skill. |

## Needed Before v1

- Add sample CSV/JSON fixtures for each production skill.
- Add one full `expected-output.md` and one `known-bad-output.md` per production skill.
- Turn the strongest stress tests into repeatable eval cases with pass/fail criteria.
- Add link checks and frontmatter checks to CI.
- Extract common Amazon PPC guardrails into shared references when duplication becomes hard to maintain.
- Confirm the license, security, and data privacy docs are visible in the README and PR template.

## Contributor Priority Levels

- `P0 safety`: approval gates, live write blockers, BSR causality, data privacy, prompt injection, and missing-data confidence.
- `P1 onboarding`: README clarity, install friction, glossary, FAQ, examples, and first-run prompts.
- `P2 skill coverage`: narrow Amazon PPC workflows that plug into the operating system.
- `P3 polish`: formatting, wording, taxonomy cleanup, and non-blocking reference improvements.

## Good First Skill Ideas

These are scoped so a PPC operator can contribute one workflow without needing to redesign the whole project.

Completed:

- `amazon-search-term-harvest-planner`: exact-match harvesting, safe source-negative routing, duplicate checks, and watchlist decisions.

Next good first skills:

1. `amazon-wasted-spend-triage`
   - Separates true waste from strategic spend, brand defense, launch support, and low-sample noise.
   - Should output bid-down, negative, pause, monitor, and investigate actions.

2. `amazon-budget-reallocation-planner`
   - Moves spend from isolated waste or blocked growth into proven winners.
   - Must preserve rank defense, brand defense, launch velocity, and inventory gates.

3. `amazon-inventory-aware-ppc-scaling`
   - Blocks or throttles scale when days of supply, inbound stock, or Featured Offer / Buy Box risk makes growth unsafe.
   - Useful for brands that over-advertise into stockouts.

4. `amazon-bsr-rank-rescue`
   - Diagnoses BSR or organic-rank deterioration and builds a recovery plan.
   - Must distinguish PPC traffic loss, conversion loss, retail readiness, competitor moves, and category demand.

5. `amazon-placement-optimization-review`
   - Reviews Top of Search, Rest of Search, and Product Pages performance.
   - Should recommend placement modifier changes only when sample size, CVR, CPC, and strategic role support it.

6. `amazon-brand-defense-audit`
   - Reviews branded and own-ASIN defensive coverage.
   - Must check incrementality before recommending expansion or reduction.

7. `amazon-product-target-expansion`
   - Mines converting product targets and purchased ASIN patterns.
   - Should separate competitor conquesting, own-ASIN defense, category adjacency, and irrelevant targets.

8. `amazon-launch-readiness-ppc-plan`
   - Builds a controlled launch plan from margin, stock, listing readiness, review position, target keywords, and budget.
   - Must include monitoring and stop-loss criteria.

9. `rocketcart-post-change-monitor`
   - Reviews approved Rocketcart changes after execution and classifies each action as worked, failed, inconclusive, or needs more data.
   - Should use readback, 3-day, 7-day, and 14-day monitoring rules.

## Advanced Skill Ideas

- Sponsored Brands growth and new-to-brand analysis.
- Sponsored Display remarketing and product targeting review.
- Marketplace expansion plan by country.
- Category competitor movement monitor.
- Variation-level traffic and conversion diagnosis.
- Listing-before-spend audit using sessions, CVR, reviews, rating, price, and content signals.
- Agency account review pack that prepares a client-facing weekly summary.

## Rocketcart MCP Direction

The first bridge skill is `rocketcart-amazon-ads-live-optimization-review`. Future Rocketcart-specific skills should follow the same read-first pattern:

1. Read live Ads state and historical analytics.
2. Join product intelligence: ASIN/SKU context, inventory, Featured Offer / Buy Box, category rank/BSR movement, price, reviews/rating, competitor signals, and product readiness where available.
3. Detect changes, risks, and opportunities.
4. Propose exact action rows.
5. Run preflight checks before any write.
6. Require explicit approval for all material changes.
7. Execute only the approved changes.
8. Read back the resulting state and define monitoring windows.

Open-source skills should describe the workflow even when Rocketcart MCP is unavailable.

## Rocketcart Upper-Funnel Goals

- Let operators prove value with static exports before they connect live tooling.
- Make Rocketcart feel like the natural next layer for live Ads reads, product intelligence, drift detection, preflight, readback, and monitoring.
- Keep trust high by making no-write-by-default behavior obvious in README, examples, evals, and Rocketcart-specific skills.
- Encourage agencies and AI builders to customize open-source skills while preserving Rocketcart-compatible action rows.
- Turn repeated contributor ideas into Rocketcart-aware workflows only when live state materially improves safety or execution quality.

## Success Signals

- Operators can install the repo and run a useful review in under 10 minutes.
- Contributors can add a new skill without asking how the repo is structured.
- Skills produce action-ready recommendations without pretending uncertain data is certain.
- Rocketcart users can graduate from static skill outputs to live guarded execution.
