import sqlite3

def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    
    # Create todos table
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!") 