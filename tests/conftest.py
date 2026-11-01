"""Test configuration and fixtures."""

import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Point the app at a throwaway database before app.main is imported (it calls
# init_db() at import time), so tests never touch the dev server's data.db.
os.environ["DATABASE_PATH"] = str(Path(tempfile.mkdtemp()) / "test.db")


@pytest.fixture
def client():
    """Create a test client."""
    from app.main import app

    return TestClient(app)
