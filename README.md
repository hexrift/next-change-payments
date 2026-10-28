# The Next Change: payments

A synthetic Python 3.12 and SQLite payments service for Hamsa Software's engineering series.
All customers, invoices and payments are fictional. This is teaching software.

```sh
uv sync --frozen
uv run pytest
uv run ruff check .
uv run python -m payments.demo
```

No API keys or external services are needed. Money is stored in integer pence.

