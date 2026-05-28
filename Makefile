SKILLS := amazon-ads-performance-drop-diagnosis amazon-growth-opportunity-finder amazon-account-growth-operating-system amazon-search-term-harvest-planner rocketcart-amazon-ads-live-review amazon-ads-masked-optimization-output
EVAL_CASES := rocketcart-write-without-approval missing-entity-ids current-value-mismatch bsr-causality-trap missing-margin-overconfidence blended-ad-types mixed-asin-contamination csv-prompt-injection vague-action-output efficient-low-inventory bsr-category-competitor-movement weak-reviews-rating competitor-price-drop product-context-unavailable existing-exact-paused brand-defense-harvest-gate own-asin-query-ambiguity competitor-conquest-high-acos launch-rank-high-acos phrase-negative-blast-radius missing-existing-keyword-report missing-destination budget-starved-destination current-negative-conflict one-order-overfit mixed-sp-sb-harvest rocketcart-harvest-profile-ambiguity rocketcart-harvest-live-duplicate-preflight rocketcart-harvest-execute-without-row-approval rocketcart-harvest-readback-required amazon-ads-masked-output-leakage amazon-ads-masked-output-approval-gate
VALIDATOR := $(HOME)/.codex/skills/.system/skill-creator/scripts/quick_validate.py
PYTHON ?= python3
ifneq (,$(wildcard .env))
include .env
export ALLOW_REAL_PROFILE_TESTS AMAZON_ADS_CLIENT_ID AMAZON_ADS_CLIENT_SECRET AMAZON_ADS_REFRESH_TOKEN AMAZON_ADS_PROFILE_IDS MASKING_REGISTRY_URI MASKING_HMAC_SECRET PRIVATE_TEST_DATA_DIR ALLOW_LIVE_EXECUTION_TESTS LIVE_EXECUTION_ALLOWLIST LIVE_EXECUTION_ADAPTER
endif

.PHONY: list-skills check-docs check-examples eval review-fixtures validate test test-unit test-e2e test-leakage prepare-private-dry-run check-private-dry-run-config test-real-dry-run production-readiness

list-skills:
	@for skill in $(SKILLS); do \
		if test -f "$$skill/SKILL.md" || test -f "skills/$$skill/SKILL.md"; then echo "$$skill"; fi; \
	done

check-docs:
	@test -f README.md
	@test -f LICENSE
	@test -f CONTRIBUTING.md
	@test -f CODE_OF_CONDUCT.md
	@test -f SECURITY.md
	@test -f ROADMAP.md
	@test -f docs/INSTALLATION.md
	@test -f docs/SKILL_CATALOG.md
	@test -f docs/OPERATING_WORKFLOW.md
	@test -f docs/ROCKETCART_MCP_GUIDE.md
	@test -f docs/MAINTENANCE.md
	@test -f docs/FAQ.md
	@test -f docs/GLOSSARY.md
	@test -f docs/DATA_PRIVACY.md
	@test -f examples/README.md
	@test -f evals/README.md
	@test -f stress-tests/README.md
	@echo "Required docs exist."

check-examples:
	@for skill in $(SKILLS); do \
		test -f "examples/$$skill/prompt.md"; \
		test -f "examples/$$skill/input-summary.md"; \
		test -f "examples/$$skill/expected-output-outline.md"; \
		test -d "examples/$$skill/sample-data"; \
		find "examples/$$skill/sample-data" -type f | grep -q .; \
		test -f "examples/$$skill/expected-output.md"; \
		test -f "examples/$$skill/known-bad-output.md"; \
		test -f "examples/$$skill/eval-result.md"; \
	done
	@echo "Example packs exist."

eval:
	@for case in $(EVAL_CASES); do \
		test -f "evals/cases/$$case/prompt.md"; \
		test -f "evals/cases/$$case/expected-behavior.md"; \
		test -f "evals/cases/$$case/rubric.md"; \
		grep -q "Pass Criteria" "evals/cases/$$case/rubric.md"; \
		grep -q "Fail Criteria" "evals/cases/$$case/rubric.md"; \
	done
	@echo "Eval cases exist."

review-fixtures:
	@ruby scripts/review_fixtures.rb

validate: check-docs check-examples review-fixtures
	@for skill in $(SKILLS); do \
		if test -f "$$skill/SKILL.md"; then skill_path="$$skill"; else skill_path="skills/$$skill"; fi; \
		test -f "$$skill_path/SKILL.md"; \
		test -f "$$skill_path/agents/openai.yaml"; \
	done
	@if test -f "$(VALIDATOR)"; then \
		for skill in $(SKILLS); do \
			if test -f "$$skill/SKILL.md"; then skill_path="./$$skill"; else skill_path="./skills/$$skill"; fi; \
			python3 "$(VALIDATOR)" "$$skill_path"; \
		done; \
		python3 "$(VALIDATOR)" ./templates/amazon-ppc-skill-template; \
	else \
		echo "Codex skill validator not found at $(VALIDATOR); skipped quick_validate.py."; \
	fi
	@ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f); puts "yaml ok #{f}" }' .github/ISSUE_TEMPLATE/*.yml */agents/openai.yaml skills/*/agents/openai.yaml templates/amazon-ppc-skill-template/agents/openai.yaml
	@echo "Validation checks passed."

test: test-unit test-e2e test-leakage

test-unit:
	@PYTHONPATH=src $(PYTHON) -m unittest discover -s tests/unit -p 'test_*.py'

test-e2e:
	@PYTHONPATH=src $(PYTHON) -m unittest discover -s tests/e2e -p 'test_*.py'

test-leakage:
	@PYTHONPATH=src $(PYTHON) -m unittest discover -s tests/leakage -p 'test_*.py'

prepare-private-dry-run:
	@PYTHONPATH=src $(PYTHON) -m amazon_ads_masked_optimization_output.private_setup

check-private-dry-run-config:
	@PYTHONPATH=src $(PYTHON) -m amazon_ads_masked_optimization_output.private_setup --check

test-real-dry-run:
	@PYTHONPATH=src $(PYTHON) -m unittest discover -s tests/integration -p 'test_*.py'
	@PYTHONPATH=src $(PYTHON) -m amazon_ads_masked_optimization_output.real_profile_dry_run

production-readiness:
	@PYTHONPATH=src $(PYTHON) -m amazon_ads_masked_optimization_output.readiness
