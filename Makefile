SHELL := /bin/sh

.DEFAULT_GOAL := help

.PHONY: help fmt format lint validate package smoke smoke-package check

help:
	@printf '%s\n' "Usage: make <target>" ""
	@printf '%s\n' "Development:"
	@printf '  %-12s %s\n' "fmt" "Normalize JSON metadata"
	@printf '  %-12s %s\n' "format" "Alias for fmt"
	@printf '  %-12s %s\n' "lint" "Run repository hygiene checks"
	@printf '  %-12s %s\n' "validate" "Validate Claude plugin manifest and layout"
	@printf '  %-12s %s\n' "package" "Build an installable plugin ZIP under dist"
	@printf '  %-12s %s\n' "smoke" "Confirm Claude discovers the bundled Endgame MCP server"
	@printf '  %-12s %s\n' "smoke-package" "Confirm Claude discovers MCP from the packaged ZIP"
	@printf '  %-12s %s\n' "check" "Run lint and validate"

fmt:
	python3 scripts/format_json.py

format: fmt

lint:
	python3 scripts/lint_repo.py

validate:
	python3 scripts/validate_plugin.py

package: check
	python3 scripts/package_plugin.py

smoke:
	python3 scripts/smoke_plugin.py

smoke-package: package
	python3 scripts/smoke_plugin.py --package

check: lint validate
