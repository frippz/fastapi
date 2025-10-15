.PHONY: env install install-dev start lint format test clean

env:
	uv venv
	make install-dev

install:
	uv pip install -r requirements.txt

install-dev:
	uv pip install -r requirements-dev.txt

start:
	uv run uvicorn app.main:app --reload

lint:
	uvx ruff check .

format:
	uvx ruff format .

test:
	uv run python -m pytest

clean:
	uv clean
