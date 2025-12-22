from datetime import datetime
from typing import Optional

from app.services.payments import get_connection

def init_crm_db() -> None:
    """
    Create tables for CRM (users, funnel events), if they do not exist.
    """
    with get_connection() as conn:
        cursor=conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                first_seen TEXT,
                last_seen TEXT
            )
        """)

    conn.commit()

def upset_user(
        user_id: int,
        username: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
) -> None:
    """
    Insert or update user info and last_seen timestamp.
    If the user is new, set first_seen as well.
    """
    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    with get_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (user_id) DO UPDATE SET
                username=excluded.username,
                first_name=excluded.first_name,
                last_name=excluded.last_name,
                last_seen=excluded.last_seen
        """,
            (user_id, username, first_name, last_name, now, now),
        )
        conn.commit()

def get_all_users() -> list[int]:
    with get_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
    return [row[0] for row in rows]