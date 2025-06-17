import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "deepresearch_sessions.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sessions (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SessionMemory (
        session_id TEXT PRIMARY KEY,
        extracted_json TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES Sessions(id)
    )
    """)

    conn.commit()
    conn.close()