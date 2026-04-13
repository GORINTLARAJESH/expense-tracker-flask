import pandas as pd


# ================= CONVERT TO DATAFRAME =================
def to_dataframe(rows):
    """
    Convert SQLite rows to Pandas DataFrame safely
    """
    if not rows:
        return pd.DataFrame()

    return pd.DataFrame([dict(row) for row in rows])


# ================= SUMMARY CALCULATIONS =================
def calculate_summary(df):
    """
    Calculate income, expense, and balance
    """
    if df.empty:
        return 0, 0, 0

    df["amount"] = df["amount"].astype(float)

    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    balance = income - expense

    return income, expense, balance


# ================= MONTHLY ANALYTICS =================
def monthly_analysis(df):
    """
    Group data by month for charts
    """
    if df.empty:
        return [], []

    df["month"] = df["date"].str[:7]

    monthly = df.groupby("month")["amount"].sum()

    return list(monthly.index), list(monthly.values)


# ================= CATEGORY ANALYTICS =================
def category_analysis(df):
    """
    Group data by category
    """
    if df.empty:
        return [], []

    category = df.groupby("category")["amount"].sum()

    return list(category.index), list(category.values)


# ================= RECENT TRANSACTIONS =================
def get_recent_transactions(rows, limit=5):
    """
    Get latest transactions
    """
    return rows[:limit]


# ================= FULL ANALYTICS PIPELINE =================
def generate_dashboard_data(rows):
    """
    One function to generate all dashboard data
    """
    df = to_dataframe(rows)

    income, expense, balance = calculate_summary(df)

    months, monthly_data = monthly_analysis(df)

    categories, category_data = category_analysis(df)

    transactions = get_recent_transactions(rows)

    return {
        "income": income,
        "expense": expense,
        "balance": balance,
        "months": months,
        "monthly_data": monthly_data,
        "categories": categories,
        "category_data": category_data,
        "transactions": transactions
    }