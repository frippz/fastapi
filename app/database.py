import sqlite3

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