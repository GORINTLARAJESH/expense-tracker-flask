# routes/budget_routes.py

from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from config import Config

budget = Blueprint('budget', __name__)


# ================= BUDGET PAGE =================
@budget.route('/budget', methods=['GET', 'POST'])
def budget_page():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(Config.DB_PATH)
    cur = conn.cursor()

    # ================= SET / UPDATE BUDGET =================
    if request.method == 'POST':
        amount = request.form.get('budget')

        try:
            amount = float(amount)

            if amount > 0:
                cur.execute("""
                    INSERT INTO budget (user_id, total_budget)
                    VALUES (?, ?)
                    ON CONFLICT(user_id)
                    DO UPDATE SET total_budget=excluded.total_budget
                """, (session['user_id'], amount))

                conn.commit()

        except (ValueError, TypeError):
            pass  # ignore invalid input

    # ================= FETCH BUDGET =================
    cur.execute("""
        SELECT total_budget
        FROM budget
        WHERE user_id=?
    """, (session['user_id'],))

    result = cur.fetchone()
    total_budget = result[0] if result else 0

    # ================= FETCH EXPENSE =================
    cur.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id=? AND type='expense'
    """, (session['user_id'],))

    spent = cur.fetchone()[0] or 0

    # ================= CALCULATIONS =================
    remaining = total_budget - spent
    percent_used = (spent / total_budget * 100) if total_budget else 0

    # ================= EXTRA ANALYTICS =================
    over_budget = spent > total_budget

    conn.close()

    return render_template(
        "budget.html",
        total_budget=total_budget,
        spent=spent,
        remaining=remaining,
        percent_used=round(percent_used, 2),
        over_budget=over_budget
    )


# ================= DELETE / RESET BUDGET =================
@budget.route('/delete_budget')
def delete_budget():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(Config.DB_PATH)
    cur = conn.cursor()

    # Option 1: DELETE budget row
    cur.execute("""
        DELETE FROM budget
        WHERE user_id=?
    """, (session['user_id'],))

    conn.commit()
    conn.close()

    return redirect('/budget')