.PHONY: install install-dev start lint format test clean

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
RUFF = $(VENV)/bin/ruff

install:
	python -m venv $(VENV)
	uv venv
	uv pip install -r requirements.txt

install-dev:
	python -m venv $(VENV)
	uv venv
	uv pip install -r requirements-dev.txt

start:
	$(UVICORN) app.main:app --reload

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

test:
	$(PYTHON) -m pytest

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
