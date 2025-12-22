import sqlite3

from app.config import (
    PAY_URL,
    DB_PATH,)

paid_users: set[int] = set()

def get_connection():
    """
    Function to get connection via SQLite3
    """
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    """
    Initialize payments database (create tables if they don't exist).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paid_users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )
    """)
    conn.commit()
    conn.close()

def mark_user_paid(
        user_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
) -> None:
    """Mark user as paid in the database.
    Also store basic user info for admin view"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO paid_users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        """,
    (user_id, username, first_name, last_name),
    )

    conn.commit()
    conn.close()

def is_paid_user(user_id: int) -> bool:
    """
    Check if user is in paid users table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 1 FROM paid_users 
        WHERE user_id = ?
        """,
        (user_id,),
    )
    row = cursor.fetchone()

    conn.close()
    return row is not None

def create_payment_link(user_id: int) -> str:
    """
    Create payment link for the given Telegram user.
    For now, it just returns PAY_URL from config,
    but later it can be replaced with real YooMoney integration
    """
    return PAY_URL

def get_all_paid_users() -> list[dict]:
    """
    Return a list of all paid users with their basic info
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id, username, first_name, last_name 
        FROM paid_users
        """,
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "user_id": row[0],
            "username": row[1],
            "first_name": row[2],
            "last_name": row[3],
        }
        for row in rows
    ]