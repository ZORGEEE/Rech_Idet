import sqlite3

def init_db():
    with open('db_new.sql', 'r', encoding='utf-8') as f:
        sql_commands = f.read()
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.executescript(sql_commands)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!") 