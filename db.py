from pathlib import Path
import sqlite3

# Always store the database beside this file, no matter where the app starts from.
BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "privsearch.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            engine TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_bookmark(title, url, engine="unknown"):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO bookmarks (title, url, engine) VALUES (?, ?, ?)",
            (title, url, engine),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_bookmarks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM bookmarks ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def delete_bookmark(bookmark_id):
    conn = get_connection()
    conn.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database ready at: {DB_NAME}")
