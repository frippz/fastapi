"""Tests for the users and posts endpoints."""

import pytest

from app.database import get_db


@pytest.fixture(autouse=True)
def cleanup_users_posts():
    """Clean up users and posts after each test."""
    yield
    with get_db() as db:
        db.execute("DELETE FROM posts")
        db.execute("DELETE FROM users")
        db.commit()


def create_user(client, email="ada@example.com"):
    response = client.post("/users/", json={"name": "Ada", "email": email})
    assert response.status_code == 201
    return response.json()


def test_duplicate_email_rejected(client):
    create_user(client)
    response = client.post(
        "/users/", json={"name": "Ada 2", "email": "ada@example.com"}
    )
    assert response.status_code == 400


def test_create_and_get_post(client):
    user = create_user(client)
    created = client.post(
        "/posts/", json={"title": "Hi", "body": "Body", "userId": user["userId"]}
    )
    assert created.status_code == 201
    assert created.json()["author"]["userId"] == user["userId"]

    response = client.get(f"/posts/{created.json()['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Hi"


def test_create_post_unknown_user(client):
    response = client.post(
        "/posts/", json={"title": "Hi", "body": "Body", "userId": "nope"}
    )
    assert response.status_code == 404


def test_delete_user_deletes_their_posts(client):
    user = create_user(client)
    client.post(
        "/posts/", json={"title": "Hi", "body": "Body", "userId": user["userId"]}
    )

    assert client.delete(f"/users/{user['userId']}").status_code == 204

    with get_db() as db:
        count = db.execute(
            "SELECT COUNT(*) FROM posts WHERE userId = ?", (user["userId"],)
        ).fetchone()[0]
    assert count == 0


def test_post_response_shape(client):
    user = create_user(client)
    post = client.post(
        "/posts/", json={"title": "Hi", "body": "Body", "userId": user["userId"]}
    ).json()
    assert post["userId"] == user["userId"]
    assert post["createdAt"].endswith("Z")


def test_posts_newest_first_within_same_second(client):
    user = create_user(client)
    ids = [
        client.post(
            "/posts/", json={"title": f"P{i}", "body": "B", "userId": user["userId"]}
        ).json()["id"]
        for i in range(3)
    ]
    listed = [p["id"] for p in client.get("/posts/").json()]
    assert listed == list(reversed(ids))
