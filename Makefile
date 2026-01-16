

setup:
	@uv sync

format:
	@uv run task format-and-lint

lint:
	@uv run task ruff-lint && uv run task mypy-lint
