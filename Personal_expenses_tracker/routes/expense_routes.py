from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models.model import (
    get_user_expenses,
    delete_expense as delete_expense_db,
    get_expense_by_id,
    update_expense as update_expense_db
)

expense = Blueprint('expense', __name__)


# ================= HELPER =================
def require_login():
    return "user_id" in session


# ================= VIEW ALL EXPENSES =================
@expense.route("/expenses")
def view_expenses():

    if not require_login():
        return redirect(url_for("auth.login"))

    rows = get_user_expenses(session["user_id"])

    return render_template(
        "expenses.html",
        expenses=rows,
        title="Expenses"
    )


# ================= DELETE EXPENSE =================
@expense.route("/delete/<int:id>")
def delete_expense(id):

    if not require_login():
        return redirect(url_for("auth.login"))

    try:
        delete_expense_db(id, session["user_id"])
        flash("🗑️ Expense deleted successfully", "success")
    except Exception:
        flash("❌ Failed to delete expense", "danger")

    return redirect(url_for("expense.view_expenses"))


# ================= EDIT EXPENSE PAGE =================
@expense.route("/edit/<int:id>")
def edit_expense(id):

    if not require_login():
        return redirect(url_for("auth.login"))

    row = get_expense_by_id(id, session["user_id"])

    if not row:
        flash("❌ Expense not found", "danger")
        return redirect(url_for("expense.view_expenses"))

    return render_template(
        "edit_expense.html",
        expense=row,
        title="Edit Expense"
    )


# ================= UPDATE EXPENSE =================
@expense.route("/update/<int:id>", methods=["POST"])
def update_expense(id):

    if not require_login():
        return redirect(url_for("auth.login"))

    # ✅ Safe form extraction
    date = request.form.get("date", "").strip()
    type_ = request.form.get("type", "").strip()
    category = request.form.get("category", "").strip()
    amount = request.form.get("amount", "").strip()

    # 🔥 Validation
    if not all([date, type_, category, amount]):
        flash("⚠️ Please fill all fields", "warning")
        return redirect(url_for("expense.edit_expense", id=id))

    if type_ not in ["income", "expense"]:
        flash("❌ Invalid type selected", "danger")
        return redirect(url_for("expense.edit_expense", id=id))

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("❌ Amount must be a positive number", "danger")
        return redirect(url_for("expense.edit_expense", id=id))

    try:
        update_expense_db(id, session["user_id"], date, type_, category, amount)
        flash("✏️ Expense updated successfully", "success")
    except Exception:
        flash("❌ Failed to update expense", "danger")

    return redirect(url_for("expense.view_expenses"))