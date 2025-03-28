"""Database module for SQLite connection and initialization."""

import sqlite3
from contextlib import contextmanager
from typing import Generator


def init_db():
    """
    Initialize the database with required tables.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Drop existing tables to ensure clean state
        cursor.execute("DROP TABLE IF EXISTS posts")
        cursor.execute("DROP TABLE IF EXISTS todos")
        cursor.execute("DROP TABLE IF EXISTS users")

        # Create users table with auto-incrementing ID and UUID userId
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                userId TEXT NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16))))
            )
        """
        )

        # Create todos table with auto-incrementing ID
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        """
        )

        # Create posts table with auto-incrementing ID and createdAt timestamp
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                userId TEXT NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (userId) REFERENCES users(userId)
            )
        """
        )

        conn.commit()


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Database context manager that creates and manages SQLite connections.
    Ensures connections are properly closed and thread-safe.

    Yields:
        sqlite3.Connection: A SQLite database connection.
    """
    conn = sqlite3.connect("data.db", check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
