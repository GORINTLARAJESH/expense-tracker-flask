# utils/helpers.py

from datetime import datetime


# ================= FORMAT CURRENCY =================
def format_currency(amount):
    """
    Convert number to ₹ format
    Example: 1000 -> ₹ 1,000.00
    """
    try:
        amount = float(amount)
        return f"₹ {amount:,.2f}"
    except (ValueError, TypeError):
        return "₹ 0.00"


# ================= FORMAT DATE =================
def format_date(date_str):
    """
    Convert YYYY-MM-DD -> DD Mon YYYY
    Example: 2026-04-05 -> 05 Apr 2026
    """
    try:
        if not date_str:
            return ""
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %b %Y")
    except (ValueError, TypeError):
        return date_str


# ================= MONTH NAME =================
def get_month_name(date_str):
    """
    Convert YYYY-MM-DD -> Mon YYYY
    Example: 2026-04-05 -> Apr 2026
    """
    try:
        if not date_str:
            return ""
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%b %Y")
    except (ValueError, TypeError):
        return date_str


# ================= SAFE FLOAT =================
def safe_float(value):
    """
    Convert value safely to float
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


# ================= CALCULATE TOTAL =================
def calculate_totals(rows):
    """
    Calculate income, expense, balance
    Works with sqlite3.Row or dict
    """
    income = 0.0
    expense = 0.0

    for r in rows:
        amount = safe_float(r["amount"])
        type_ = str(r["type"]).lower()

        if type_ == "income":
            income += amount
        elif type_ == "expense":
            expense += amount

    balance = income - expense

    return income, expense, balance


# ================= VALIDATE EXPENSE FORM =================
def validate_expense_form(data):
    """
    Validate expense form input
    Returns list of errors
    """
    errors = []

    date = data.get("date", "").strip()
    type_ = data.get("type", "").strip()
    category = data.get("category", "").strip()
    amount = data.get("amount", "").strip()

    if not date:
        errors.append("Date is required")

    if type_ not in ["income", "expense"]:
        errors.append("Invalid type selected")

    if not category:
        errors.append("Category is required")

    try:
        amount = float(amount)
        if amount <= 0:
            errors.append("Amount must be greater than 0")
    except (ValueError, TypeError):
        errors.append("Invalid amount")

    return errors