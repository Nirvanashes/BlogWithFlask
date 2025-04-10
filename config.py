import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("FLASK_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", "sqlite:///posts.db")
    MAIL_ADDRESS = os.environ.get("EMAIL_KEY")
    MAIL_PASSWORD = os.environ.get("PASSWORD_KEY")