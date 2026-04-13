from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models.model import get_user_expenses, add_expense as add_expense_db
from services.analytics import generate_dashboard_data

dashboard = Blueprint('dashboard', __name__)


# ================= DASHBOARD =================
@dashboard.route("/dashboard")
def dashboard_home():

    # 🔐 Check login
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # ✅ Get user data
    rows = get_user_expenses(session["user_id"])

    # ✅ Use service layer (BEST PRACTICE)
    data = generate_dashboard_data(rows)

    return render_template("dashboard.html", **data)


# ================= ADD EXPENSE PAGE =================
@dashboard.route("/add_expense")
def add_expense_page():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("add_expense.html")


# ================= SAVE EXPENSE =================
@dashboard.route("/add", methods=["POST"])
def add_expense():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # ✅ Get form data safely
    date = request.form.get("date")
    type_ = request.form.get("type")
    category = request.form.get("category")
    amount = request.form.get("amount")

    # 🔥 Validation
    if not date or not type_ or not category or not amount:
        flash("⚠️ Please fill all fields")
        return redirect(url_for("dashboard.add_expense_page"))

    try:
        amount = float(amount)
    except ValueError:
        flash("❌ Invalid amount")
        return redirect(url_for("dashboard.add_expense_page"))

    # ✅ Save using model
    add_expense_db(session["user_id"], date, type_, category, amount)

    flash("✅ Expense added successfully")

    return redirect(url_for("dashboard.dashboard_home"))