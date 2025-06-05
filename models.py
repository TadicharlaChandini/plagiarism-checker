import sqlite3

def init_db():
    conn = sqlite3.connect('plagiarism.db')
    c = conn.cursor()

    # 1. Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 2. Uploads table
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 3. Reports table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upload_id INTEGER,
            compared_with TEXT,
            similarity_score REAL,
            report_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (upload_id) REFERENCES uploads(id)
        )
    ''')

    conn.commit()
    conn.close()

# Run this once to create the database and tables
if __name__ == '__main__':
    init_db()
