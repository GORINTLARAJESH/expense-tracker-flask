# app.py

from flask import Flask, jsonify, session
from config import Config
import os
import sqlite3

# 🔗 Import Blueprints
from routes.auth_routes import auth
from routes.dashboard_routes import dashboard
from routes.expense_routes import expense
from routes.income_routes import income
from routes.budget_routes import budget
from routes.goals_routes import goals

# 🔗 Import helpers
from utils.helpers import (
    format_currency,
    format_date,
    get_month_name
)


# ================= APP FACTORY =================
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # ✅ Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # ✅ Load config
    app.config.from_object(Config)

    # 🔐 Secret key
    app.secret_key = app.config.get("SECRET_KEY", "dev_secret_key")

    # ================= REGISTER BLUEPRINTS =================
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(expense)
    app.register_blueprint(income)
    app.register_blueprint(budget)
    app.register_blueprint(goals)

    # ================= JINJA GLOBALS =================
    app.jinja_env.globals.update(
        format_currency=format_currency,
        format_date=format_date,
        get_month_name=get_month_name
    )

    # ================= DATABASE INIT =================
    from create_db import create_tables
    create_tables()

    # ================= CHART API =================
    @app.route("/api/chart-data")
    def chart_data():
        if "user_id" not in session:
            return jsonify({
                "months": [],
                "monthly_data": [],
                "categories": [],
                "category_data": []
            })

        conn = sqlite3.connect(Config.DB_PATH)
        cur = conn.cursor()

        # 📊 Monthly Expenses
        cur.execute("""
            SELECT strftime('%m', date) AS month, SUM(amount)
            FROM expenses
            WHERE user_id=? AND type='expense'
            GROUP BY month
            ORDER BY month
        """, (session['user_id'],))

        monthly_rows = cur.fetchall()

        months = []
        monthly_data = []

        for m, total in monthly_rows:
            months.append(get_month_name(m))   # helper function
            monthly_data.append(total or 0)

        # 📊 Category Expenses
        cur.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id=? AND type='expense'
            GROUP BY category
        """, (session['user_id'],))

        category_rows = cur.fetchall()

        categories = [row[0] for row in category_rows]
        category_data = [row[1] for row in category_rows]

        conn.close()

        return jsonify({
            "months": months,
            "monthly_data": monthly_data,
            "categories": categories,
            "category_data": category_data
        })

    return app


# ================= RUN =================
app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", True))