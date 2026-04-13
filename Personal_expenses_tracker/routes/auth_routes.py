from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from models.model import get_user_by_username, create_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


# ================= LOGIN =================
@auth.route("/", methods=["GET", "POST"])
def login():

    # 🔐 If already logged in → go to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard_home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Basic validation
        if not username or not password:
            flash("⚠️ Please fill all fields")
            return redirect(url_for("auth.login"))

        user = get_user_by_username(username)

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard.dashboard_home"))
        else:
            flash("❌ Invalid username or password")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


# ================= REGISTER =================
@auth.route("/register", methods=["GET", "POST"])
def register():

    # 🔐 Prevent logged-in users from accessing register
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard_home"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if not username or not email or not password or not confirm_password:
            flash("⚠️ Please fill all fields")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("❌ Passwords do not match")
            return redirect(url_for("auth.register"))

        # Check existing user
        existing = get_user_by_username(username)

        if existing:
            flash("⚠️ Username already exists")
            return redirect(url_for("auth.register"))

        # 🔐 Hash password
        hashed_password = generate_password_hash(password)

        create_user(username, email, hashed_password)

        flash("✅ Registration successful! Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ================= LOGOUT =================
@auth.route("/logout")
def logout():
    session.clear()
    flash("👋 Logged out successfully")
    return redirect(url_for("auth.login"))