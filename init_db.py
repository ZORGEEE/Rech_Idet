import sqlite3

def init_db():
    # Read SQL commands from db.sql
    with open('db.sql', 'r', encoding='utf-8') as f:
        sql_commands = f.read()
    
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Execute SQL commands
    cursor.executescript(sql_commands)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!") 