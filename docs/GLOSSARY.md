# Glossary

## Codex Skill

A folder with a `SKILL.md` file that gives Codex specialized instructions for a task. In this repo, each top-level skill folder teaches an Amazon PPC workflow.

## Claude Skill

A skill folder uploaded to Claude so Claude can use the instructions in `SKILL.md`. Upload one skill folder at a time, not the whole repository.

## MCP

Model Context Protocol. MCP lets an AI assistant use approved external context and action capabilities through a structured interface.

## Rocketcart MCP

Rocketcart's MCP layer for Amazon Ads reads, product intelligence, optimization snapshots, live-state checks, guarded writes, and readback. It is optional; the open-source skills also work with static exports.

## Product Intelligence

Product-level context that changes PPC decisions, such as ASIN/SKU mapping, inventory or availability, Featured Offer / Buy Box, price, reviews, rating, category rank/BSR movement, estimated demand, competitor changes, seasonal context, and margin or target ACoS when available.

## Optimization Memory

Rocketcart context about prior optimization sessions, snapshots, changelogs, entity history, pending evaluations, cooldowns, and recent live drift. It helps avoid repeating actions that are already under evaluation or recently failed.

## Preflight

A live check immediately before a proposed write. It verifies exact entity IDs, current values, profile/account, eligibility, and safety blockers.

## Readback

A live check after an approved write to confirm what actually changed.

## T-1

The latest fully completed reporting day. Use T-1 when same-day Amazon Ads or retail data may be incomplete.

## BSR

Best Seller Rank. Lower is better. BSR is category-relative and should be treated as a velocity signal, not proof that ads caused organic growth.

## TACoS

Total Advertising Cost of Sales: ad spend divided by total sales. It requires total sales for the same product/account scope and date window.

## Featured Offer / Buy Box

The offer Amazon features for purchase. If a product loses Featured Offer / Buy Box, ad traffic may stop converting or become unsafe to scale.

## Action Gate

A safety check that decides whether a recommendation is action-safe, directional, or not actionable.

## Watchlist

A finding that is worth monitoring but not ready for execution because evidence is thin, data is missing, or risk is high.

## Approval-Gated Action

A proposed live change that requires human approval before execution.

## Exact Entity ID

The stable Amazon Ads identifier for a campaign, ad group, keyword, target, or negative. Names alone are not enough for live writes.
