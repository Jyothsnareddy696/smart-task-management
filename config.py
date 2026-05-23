import os

class Config:
    # Better security practice
    SECRET_KEY = os.getenv("SECRET_KEY", "task_secret_key")

    # PostgreSQL connection (can be overridden using environment variable)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:jyo123@localhost/task_manager"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False