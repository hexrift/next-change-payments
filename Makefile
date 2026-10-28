.PHONY: test lint demo
test:
	uv run --frozen pytest
lint:
	uv run --frozen ruff check .
demo:
	uv run --frozen python -m payments.demo
