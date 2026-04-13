# routes/income_routes.py

from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from config import Config

income = Blueprint('income', __name__)


# ================= INCOME PAGE =================
@income.route('/income', methods=['GET', 'POST'])
def income_page():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(Config.DB_PATH)
    cur = conn.cursor()

    # ================= ADD INCOME =================
    if request.method == 'POST':
        source = request.form.get('source')
        amount = request.form.get('amount')
        date = request.form.get('date')

        if source and amount and date:
            try:
                amount = float(amount)

                cur.execute("""
                    INSERT INTO expenses (user_id, date, type, category, amount)
                    VALUES (?, ?, 'income', ?, ?)
                """, (session['user_id'], date, source, amount))

                conn.commit()

            except (ValueError, TypeError):
                pass  # ignore invalid input

    # ================= FETCH INCOME =================
    cur.execute("""
        SELECT id, date, category, amount
        FROM expenses
        WHERE user_id=? AND type='income'
        ORDER BY date DESC
    """, (session['user_id'],))

    incomes = cur.fetchall()

    # ================= ANALYTICS =================

    # 🔹 Total income
    cur.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id=? AND type='income'
    """, (session['user_id'],))
    total_income = cur.fetchone()[0] or 0

    # 🔹 Number of entries
    cur.execute("""
        SELECT COUNT(*)
        FROM expenses
        WHERE user_id=? AND type='income'
    """, (session['user_id'],))
    total_entries = cur.fetchone()[0]

    # 🔹 Monthly income trend
    cur.execute("""
        SELECT strftime('%m', date) AS month, SUM(amount)
        FROM expenses
        WHERE user_id=? AND type='income'
        GROUP BY month
        ORDER BY month
    """, (session['user_id'],))

    monthly_rows = cur.fetchall()

    # Format for chart
    months = [row[0] for row in monthly_rows]
    monthly_income = [row[1] for row in monthly_rows]

    conn.close()

    return render_template(
        'income.html',
        incomes=incomes,
        total_income=total_income,
        total_entries=total_entries,
        months=months,
        monthly_income=monthly_income
    )


# ================= DELETE INCOME =================
@income.route('/delete_income/<int:id>')
def delete_income(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(Config.DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM expenses
        WHERE id=? AND user_id=? AND type='income'
    """, (id, session['user_id']))

    conn.commit()
    conn.close()

    return redirect('/income')