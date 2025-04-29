import sqlite3
from config import DB_NAME

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        points INTEGER DEFAULT 0,
        referred_by INTEGER,
        last_mine INTEGER DEFAULT 0
    )
    """)
    conn.commit()

def add_user(user_id: int, name: str, referred_by: int = None):
    cur.execute("INSERT OR IGNORE INTO users(user_id, name, referred_by) VALUES (?, ?, ?)", (user_id, name, referred_by))
    conn.commit()

def get_user(user_id: int):
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cur.fetchone()

def update_points(user_id: int, points_to_add: int):
    cur.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points_to_add, user_id))
    conn.commit()

def update_last_mine(user_id: int, timestamp: int):
    cur.execute("UPDATE users SET last_mine = ? WHERE user_id = ?", (timestamp, user_id))
    conn.commit()

def count_referrals(user_id: int):
    cur.execute("SELECT COUNT(*) FROM users WHERE referred_by = ?", (user_id,))
    return cur.fetchone()[0]
