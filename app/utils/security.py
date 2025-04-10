from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


def generate_password(password):
    return generate_password_hash(
        password=password,
        method='pbkdf2:sha256',
        salt_length=16
    )


def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)


def is_admin(user):
    return user.is_authenticated and user.id == 1
