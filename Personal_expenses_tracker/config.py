# config.py

import os


class Config:
    # ================= BASE PATH =================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

    # ================= SECURITY =================
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")

    # ================= DATABASE =================
    # ✅ FIXED: Use DB_PATH (matches your app.py & routes)
    DB_PATH = os.path.join(INSTANCE_DIR, "expense.db")

    # ================= DEBUG =================
    DEBUG = True

    # ================= SESSION =================
    SESSION_PERMANENT = False