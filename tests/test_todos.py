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
    assert isinstance(data, list)
    assert len(data) > 0
    assert "task" in data[0]
    assert "id" in data[0]
    assert "completed" in data[0]


def test_toggle_todo_completion(client):
    """Test toggling a todo's completion status."""
    # Create a todo
    create_response = client.post("/todos/", json={"task": "Test todo", "completed": False})
    todo_id = create_response.json()["id"]

    # Toggle completion to true
    update_response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    # Toggle completion back to false
    update_response = client.put(f"/todos/{todo_id}", json={"completed": False})
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is False


def test_create_todo_with_completion_status(client):
    """Test creating a todo with specific completion status."""
    # Create a completed todo
    response = client.post("/todos/", json={"task": "Completed todo", "completed": True})
    assert response.status_code == 201
    assert response.json()["completed"] is True

    # Create an incomplete todo
    response = client.post("/todos/", json={"task": "Incomplete todo", "completed": False})
    assert response.status_code == 201
    assert response.json()["completed"] is False


def test_update_todo_partial_fields(client):
    """Test updating a todo with partial fields."""
    # Create a todo
    create_response = client.post("/todos/", json={"task": "Original task", "completed": False})
    todo_id = create_response.json()["id"]

    # Update only completion status
    update_response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True
    assert update_response.json()["task"] == "Original task"

    # Update only task
    update_response = client.put(f"/todos/{todo_id}", json={"task": "Updated task"})
    assert update_response.status_code == 200
    assert update_response.json()["task"] == "Updated task"
    assert update_response.json()["completed"] is True


def test_batch_update_todos(client):
    """Test updating multiple todos in a single request."""
    # Create multiple todos
    todo1 = client.post("/todos/", json={"task": "Todo 1", "completed": False}).json()
    todo2 = client.post("/todos/", json={"task": "Todo 2", "completed": False}).json()
    todo3 = client.post("/todos/", json={"task": "Todo 3", "completed": False}).json()

    # Update todos in batch
    updates = [
        {"id": todo1["id"], "completed": True},
        {"id": todo2["id"], "task": "Updated Todo 2"},
        {"id": todo3["id"], "completed": True, "task": "Updated Todo 3"},
    ]
    response = client.put("/todos/batch", json=updates)
    assert response.status_code == 200
    updated_todos = response.json()

    # Verify updates
    assert len(updated_todos) == 3
    assert updated_todos[0]["id"] == todo1["id"]
    assert updated_todos[0]["completed"] is True
    assert updated_todos[0]["task"] == "Todo 1"  # Task should remain unchanged

    assert updated_todos[1]["id"] == todo2["id"]
    assert updated_todos[1]["task"] == "Updated Todo 2"
    assert updated_todos[1]["completed"] is False  # Completed should remain unchanged

    assert updated_todos[2]["id"] == todo3["id"]
    assert updated_todos[2]["task"] == "Updated Todo 3"
    assert updated_todos[2]["completed"] is True


def test_batch_update_nonexistent_todo(client):
    """Test batch update with a non-existent todo."""
    # Create a todo
    todo = client.post("/todos/", json={"task": "Test todo", "completed": False}).json()

    # Try to update with a non-existent todo ID
    updates = [
        {"id": todo["id"], "completed": True},
        {"id": 999, "task": "This should fail"},
    ]
    response = client.put("/todos/batch", json=updates)
    assert response.status_code == 404
    assert "Todo with id 999 not found" in response.json()["detail"]
