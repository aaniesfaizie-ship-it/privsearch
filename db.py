import sqlite3

DB_NAME = "privsearch.db"


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
            (title, url, engine)
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
    print("Database ready.")

    add_bookmark("Python Docs", "https://docs.python.org", "google")
    add_bookmark("Learn Python", "https://learnpython.org", "bing")

    print("\nSaved bookmarks:")
    for row in get_bookmarks():
        print(f"  {row['id']}. {row['title']}  ->  {row['url']}  ({row['engine']})")
   

