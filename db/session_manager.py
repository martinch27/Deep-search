#  db/session_manager.py

import sqlite3
import os
import uuid
import json
from typing import List, Dict
from deep_researcher.utils.id_utils import generate_session_id

DB_PATH = os.path.join(os.path.dirname(__file__), "deepresearch_sessions.db")


class SessionManager:
    def __init__(self, session_id: str = None):
        self.session_id = session_id or generate_session_id()
        self.conn = sqlite3.connect(DB_PATH)
        self.ensure_session_exists()

    def ensure_session_exists(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO Sessions (id) VALUES (?)", (self.session_id,))
        cursor.execute("INSERT OR IGNORE INTO SessionMemory (session_id, extracted_json) VALUES (?, ?)",
                        (self.session_id, json.dumps([], ensure_ascii=False)))
        self.conn.commit()

    def append_extracted_items(self, new_items: List[Dict[str, str]]):
        cursor = self.conn.cursor()
        cursor.execute("SELECT extracted_json FROM SessionMemory WHERE session_id = ?", (self.session_id,))
        row = cursor.fetchone()
        if row:
            current_data = json.loads(row[0])
        else:
            current_data = []

        updated_data = current_data + new_items
        cursor.execute("""
            UPDATE SessionMemory 
            SET extracted_json = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE session_id = ?
        """, (json.dumps(updated_data, ensure_ascii=False), self.session_id))
        self.conn.commit()

    def load_extracted_items(self) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT extracted_json FROM SessionMemory WHERE session_id = ?", (self.session_id,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return []

    def close(self):
        self.conn.close()