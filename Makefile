.PHONY: env install install-dev start start-prod lint format test clean docker-build docker-run

env:
	uv venv
	make install-dev

install:
	uv pip install -r requirements.txt

install-dev:
	uv pip install -r requirements-dev.txt

start:
	uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

start-prod:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

lint:
	uvx ruff check .

format:
	uvx ruff format .

test:
	uv run python -m pytest

docker-build:
	docker build -t fastapi-demo .

docker-run:
	docker run -p 8000:8000 fastapi-demo

clean:
	uv clean
