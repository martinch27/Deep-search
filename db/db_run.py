# scripts/init_database.py

from session_schema import init_db

if __name__ == "__main__":
    init_db()
    print("✅ База данных успешно создана: deepresearch_sessions.db")