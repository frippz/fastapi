"""Database module for SQLite connection and initialization."""

import sqlite3


def init_db():
    """
    Initialize the database with required tables.
    """
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    # Drop existing tables to ensure clean state
    c.execute("DROP TABLE IF EXISTS posts")
    c.execute("DROP TABLE IF EXISTS todos")
    c.execute("DROP TABLE IF EXISTS users")

    # Create users table with auto-incrementing ID and UUID user_id
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            user_id TEXT NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16))))
        )
    """
    )

    # Create todos table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """
    )

    # Create posts table with auto-incrementing ID
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            user_id TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """
    )

    conn.commit()
    conn.close()


def get_db():
    """
    Database dependency that creates and manages SQLite connections.

    Yields:
        sqlite3.Connection: A SQLite database connection.
    """
    conn = sqlite3.connect("data.db")
    try:
        yield conn
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
