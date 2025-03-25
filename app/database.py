"""Database module for SQLite connection and initialization."""

import sqlite3


def init_db():
    """
    Initialize the database with required tables.
    """
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()

    # Drop existing tables to ensure clean state
    c.execute('DROP TABLE IF EXISTS posts')
    c.execute('DROP TABLE IF EXISTS todos')

    # Create todos table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """
    )

    # Create posts table with auto-generated UUID
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            title TEXT NOT NULL,
            body TEXT NOT NULL
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
    conn = sqlite3.connect("todos.db")
    try:
        yield conn
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
