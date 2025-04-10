from functools import wraps
from flask import abort
from flask_login import current_user
import smtplib
from config import Config


def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user != 1:
            return abort(403)
        return f(*args, **kwargs)

    return wrapper


def send_email(name, email, message):
    email_message = f"Subject:NEW CONTACT\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(Config.MAIL_ADDRESS, Config.MAIL_PASSWORD)
        connection.sendmail(Config.MAIL_ADDRESS, Config.MAIL_ADDRESS, email_message)
