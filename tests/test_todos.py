"""Tests for the todos endpoints."""


def test_create_todo(client):
    """Test creating a new todo."""
    response = client.post("/todos/", json={"task": "Test todo", "completed": False})
    assert response.status_code == 201
    data = response.json()
    assert data["task"] == "Test todo"
    assert data["completed"] is False
    assert "id" in data


def test_get_todos(client):
    """Test getting all todos."""
    # First create a todo
    client.post("/todos/", json={"task": "Test todo", "completed": False})

    # Then get all todos
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert "todos" in data
    assert isinstance(data["todos"], list)
    assert len(data["todos"]) > 0
    assert "task" in data["todos"][0]
    assert "id" in data["todos"][0]
