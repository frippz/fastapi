.PHONY: install install-dev start lint format test clean

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
RUFF = $(VENV)/bin/ruff

install:
	uv venv
	uv pip install -r requirements.txt

install-dev:
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
