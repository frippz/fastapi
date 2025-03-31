"""Script to migrate database with renamed columns."""

import sqlite3
from pathlib import Path


def migrate_database():
    """Migrate the database by renaming columns."""
    db_path = Path("data.db")
    
    if not db_path.exists():
        print("Error: data.db not found!")
        return
    
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        
        print("Starting database migration...")
        
        # Create new users table with renamed column
        print("Creating new users table...")
        cursor.execute("""
            CREATE TABLE users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                userId TEXT NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16))))
            )
        """)
        
        # Copy data from old to new users table
        print("Migrating users data...")
        cursor.execute("""
            INSERT INTO users_new (id, name, email, userId)
            SELECT id, name, email, user_id FROM users
        """)
        
        # Create new posts table with renamed columns
        print("Creating new posts table...")
        cursor.execute("""
            CREATE TABLE posts_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                userId TEXT NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (userId) REFERENCES users_new(userId)
            )
        """)
        
        # Copy data from old to new posts table
        print("Migrating posts data...")
        cursor.execute("""
            INSERT INTO posts_new (id, title, body, userId, createdAt)
            SELECT id, title, body, user_id, created_at FROM posts
        """)
        
        # Drop old tables
        print("Dropping old tables...")
        cursor.execute("DROP TABLE posts")
        cursor.execute("DROP TABLE users")
        
        # Rename new tables to original names
        print("Renaming new tables...")
        cursor.execute("ALTER TABLE users_new RENAME TO users")
        cursor.execute("ALTER TABLE posts_new RENAME TO posts")
        
        # Commit changes
        conn.commit()
        print("Migration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    migrate_database() 