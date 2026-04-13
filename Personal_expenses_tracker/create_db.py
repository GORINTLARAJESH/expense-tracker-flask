# create_db.py

import sqlite3
import os
from config import Config   # ✅ Use same config


# ================= PATH SETUP =================
DB_PATH = Config.DB_PATH

# ✅ Ensure instance folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def create_tables():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # ✅ Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON")

        # ================= USERS TABLE =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password TEXT NOT NULL
        )
        """)

        # ================= EXPENSES TABLE =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        # ================= BUDGET TABLE =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            total_budget REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        # ================= GOALS TABLE =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            saved_amount REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        print("✅ Database & tables created successfully!")

    except sqlite3.Error as e:
        print("❌ Database error:", e)

    finally:
        if conn:
            conn.close()


# ================= RUN =================
if __name__ == "__main__":
    create_tables()