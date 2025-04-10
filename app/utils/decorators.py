from functools import wraps
from flask import abort
from flask_login import current_user
from app.utils.security import is_admin


def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_admin(current_user):
            return abort(403)
        return f(*args, **kwargs)

    return wrapper
