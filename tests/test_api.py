"""Integration tests for the FastAPI application endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint returns correct response structure."""
    response = client.get("/")
    assert response.status_code == 200
    assert "title" in response.json()
    assert "version" in response.json()


def test_create_and_get_post():
    """Test creating a post and retrieving it by ID."""
    # Create a test post
    post_data = {"title": "Test Post", "body": "This is a test post"}
    response = client.post("/posts", json=post_data)
    assert response.status_code == 200
    post_id = response.json()["id"]

    # Get the created post
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == post_data["title"]
    assert response.json()["body"] == post_data["body"]


def test_create_and_get_todo():
    """Test creating a todo and retrieving it from the list."""
    # Create a test todo
    response = client.post("/todos?task=Test%20Todo")
    assert response.status_code == 200

    # Get all todos and verify
    response = client.get("/todos")
    assert response.status_code == 200
    todos = response.json()["todos"]
    assert any(todo["task"] == "Test Todo" for todo in todos)
