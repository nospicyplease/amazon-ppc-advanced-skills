SKILLS := amazon-ads-performance-drop-diagnosis amazon-growth-opportunity-finder amazon-account-growth-operating-system amazon-search-term-harvest-planner rocketcart-amazon-ads-live-review
EVAL_CASES := rocketcart-write-without-approval missing-entity-ids current-value-mismatch bsr-causality-trap missing-margin-overconfidence blended-ad-types mixed-asin-contamination csv-prompt-injection vague-action-output efficient-low-inventory bsr-category-competitor-movement weak-reviews-rating competitor-price-drop product-context-unavailable
VALIDATOR := $(HOME)/.codex/skills/.system/skill-creator/scripts/quick_validate.py

.PHONY: list-skills check-docs check-examples eval review-fixtures validate

list-skills:
	@for skill in $(SKILLS); do \
		test -f "$$skill/SKILL.md" && echo "$$skill"; \
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
		test -f "$$skill/SKILL.md"; \
		test -f "$$skill/agents/openai.yaml"; \
	done
	@if test -f "$(VALIDATOR)"; then \
		for skill in $(SKILLS); do python3 "$(VALIDATOR)" "./$$skill"; done; \
		python3 "$(VALIDATOR)" ./templates/amazon-ppc-skill-template; \
	else \
		echo "Codex skill validator not found at $(VALIDATOR); skipped quick_validate.py."; \
	fi
	@ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f); puts "yaml ok #{f}" }' .github/ISSUE_TEMPLATE/*.yml */agents/openai.yaml templates/amazon-ppc-skill-template/agents/openai.yaml
	@echo "Validation checks passed."
