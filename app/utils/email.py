from flask_mail import Message
from flask import render_template
from app.extensions import mail
from config import Config


def send_email(to, subject, template, **kwargs):
    msg = Message(
        subject=subject,
        sender=Config.MAIL_DEFAULT_SENDER,
        recipients=[to]
    )
    msg.body = "hhhhh"
    # msg.html = render_template(template, **kwargs)
    mail.send(msg)


def send_contract_notification(name, email, message):
    subject = f"New contract from {name}"
    send_email(
        to=Config.MAIL_DEFAULT_SENDER,
        subject=subject,
        # template="email/contact_notification.html",
    )
