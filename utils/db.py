"""
Lightweight SQLite wrapper for the Text Simplifier app.

Provides:
- init_db()                -> Create DB + tables if missing
- save_user_selection()    -> Upsert user selection (page-level)
- load_user_selection()    -> Read a selection
- close_db()               -> (optional) explicit cleanup

This module opens a *new* connection per call to avoid cross-thread
issues inside Streamlit. It uses WAL mode and reasonable timeouts to
reduce lock contention.
"""

import sqlite3
import os
from typing import Optional, Any

DB_PATH = os.path.join(os.getcwd(), "user_data.db")
TABLE_SQL = """
CREATE TABLE IF NOT EXISTS user_selections (
    user TEXT NOT NULL,
    page TEXT NOT NULL,
    selected TEXT,
    PRIMARY KEY(user, page)
);
"""

# SQLite connection kwargs used by each call
_CONN_KWARGS = {
    "timeout": 30,          # seconds
    "check_same_thread": False,
    "isolation_level": None,  # autocommit mode so we control transactions explicitly
}


def _get_conn():
    """Create and return a new sqlite3.Connection with recommended pragmas."""
    conn = sqlite3.connect(DB_PATH, **_CONN_KWARGS)
    # Apply pragmatic settings for concurrent reads/writes
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database and create required tables."""
    # Ensure directory exists (DB_PATH could be in subfolders in other setups)
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = _get_conn()
    try:
        with conn:
            conn.execute(TABLE_SQL)
    finally:
        conn.close()


def save_user_selection(user: str, page: str, selected: str) -> None:
    """
    Upsert a user's selection for a page.

    Args:
        user: user id / name (use 'guest' when anonymous)
        page: page identifier (e.g., 'examples' or 'spacing_examples')
        selected: a string representing selection (e.g., 'left' / 'right')
    """
    if not user:
        user = "guest"
    conn = _get_conn()
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO user_selections(user, page, selected)
                VALUES (?, ?, ?)
                ON CONFLICT(user, page) DO UPDATE SET selected=excluded.selected;
                """,
                (user, page, selected),
            )
    finally:
        conn.close()


def load_user_selection(user: str, page: str) -> Optional[str]:
    """
    Load a previously saved user selection.

    Returns:
        selected string or None if missing.
    """
    if not user:
        user = "guest"
    conn = _get_conn()
    try:
        cur = conn.execute(
            "SELECT selected FROM user_selections WHERE user=? AND page=?",
            (user, page),
        )
        row = cur.fetchone()
        return row["selected"] if row else None
    finally:
        conn.close()


def delete_user_selection(user: str, page: str) -> None:
    """Optional helper to delete a stored selection."""
    if not user:
        user = "guest"
    conn = _get_conn()
    try:
        with conn:
            conn.execute(
                "DELETE FROM user_selections WHERE user=? AND page=?",
                (user, page),
            )
    finally:
        conn.close()


# Initialize DB on import (safe & idempotent)
init_db()
