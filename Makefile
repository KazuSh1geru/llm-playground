.PHONY: format
format:
	poetry run black src
	poetry run ruff check src --fix-only --unsafe-fixes

