# models/model.py

import sqlite3
from config import Config

DB_PATH = Config.DB_PATH


# ================= DATABASE CONNECTION =================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ================= USER FUNCTIONS =================

def create_user(username, email, password):
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
    finally:
        conn.close()


def get_user_by_username(username):
    try:
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
        return user
    finally:
        conn.close()


# ❌ Removed validate_user (not secure)
# Use check_password_hash in auth_routes


# ================= EXPENSE FUNCTIONS =================

def add_expense(user_id, date, type_, category, amount):
    try:
        conn = get_db()
        conn.execute(
            """INSERT INTO expenses (user_id, date, type, category, amount)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, date, type_, category, amount)
        )
        conn.commit()
    finally:
        conn.close()


def get_user_expenses(user_id):
    try:
        conn = get_db()
        rows = conn.execute(
            "SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC",
            (user_id,)
        ).fetchall()
        return rows
    finally:
        conn.close()


def delete_expense(expense_id, user_id):
    try:
        conn = get_db()
        conn.execute(
            "DELETE FROM expenses WHERE id=? AND user_id=?",
            (expense_id, user_id)
        )
        conn.commit()
    finally:
        conn.close()


def get_expense_by_id(expense_id, user_id):
    try:
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM expenses WHERE id=? AND user_id=?",
            (expense_id, user_id)
        ).fetchone()
        return row
    finally:
        conn.close()


def update_expense(expense_id, user_id, date, type_, category, amount):
    try:
        conn = get_db()
        conn.execute(
            """UPDATE expenses
               SET date=?, type=?, category=?, amount=?
               WHERE id=? AND user_id=?""",
            (date, type_, category, amount, expense_id, user_id)
        )
        conn.commit()
    finally:
        conn.close()