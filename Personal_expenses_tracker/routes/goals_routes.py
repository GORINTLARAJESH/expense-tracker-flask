# routes/goals_routes.py

from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from config import Config

goals = Blueprint('goals', __name__)


# ================= GOALS PAGE =================
@goals.route('/goals', methods=['GET', 'POST'])
def goals_page():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(Config.DB_PATH)
    cur = conn.cursor()

    # ================= ADD GOAL =================
    if request.method == 'POST':
        name = request.form.get('name')
        target = request.form.get('target')
        saved = request.form.get('saved', 0)

        try:
            target = float(target)
            saved = float(saved)

            if name and target > 0:
                cur.execute("""
                    INSERT INTO goals (user_id, goal_name, target_amount, saved_amount)
                    VALUES (?, ?, ?, ?)
                """, (session['user_id'], name, target, saved))

                conn.commit()

        except (ValueError, TypeError):
            pass  # ignore invalid input

    # ================= FETCH GOALS =================
    cur.execute("""
        SELECT id, goal_name, target_amount, saved_amount
        FROM goals
        WHERE user_id=?
        ORDER BY id DESC
    """, (session['user_id'],))

    rows = cur.fetchall()

    # ================= FORMAT DATA =================
    goals_data = []
    for g in rows:
        percent = (g[3] / g[2]) * 100 if g[2] > 0 else 0

        goals_data.append({
            "id": g[0],
            "name": g[1],
            "target": g[2],
            "saved": g[3],
            "percent": round(percent, 2)
        })

    # ================= ANALYTICS =================
    total_goals = len(goals_data)
    completed_goals = len([g for g in goals_data if g["percent"] >= 100])

    conn.close()

    return render_template(
        'goals.html',
        goals=goals_data,
        total_goals=total_goals,
        completed_goals=completed_goals
    )


# ================= UPDATE GOAL (ADD MONEY) =================
@goals.route('/update_goal/<int:id>', methods=['POST'])
def update_goal(id):
    if 'user_id' not in session:
        return redirect('/login')

    amount = request.form.get('amount')

    try:
        amount = float(amount)

        if amount > 0:
            conn = sqlite3.connect(Config.DB_PATH)
            cur = conn.cursor()

            cur.execute("""
                UPDATE goals
                SET saved_amount = saved_amount + ?
                WHERE id=? AND user_id=?
            """, (amount, id, session['user_id']))

            conn.commit()
            conn.close()

    except (ValueError, TypeError):
        pass

    return redirect('/goals')


# ================= DELETE GOAL =================
@goals.route('/delete_goal/<int:id>')
def delete_goal(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(Config.DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM goals
        WHERE id=? AND user_id=?
    """, (id, session['user_id']))

    conn.commit()
    conn.close()

    return redirect('/goals')