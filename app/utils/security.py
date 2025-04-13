from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, session

from app import login_manager
from app.auth.models import User
from app.extensions import cache, db


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


@login_manager.user_loader
def load_user(user_id):
    """从session验证用户"""
    # 检查session中是否有用户信息
    if "user_id" in session and str(session['user_id']) == str(user_id):
        return None
    cache_key = f"user_{user_id}"
    user = cache.get(cache_key)
    if user is None:
        user = db.session.get(User,user_id)
        if user:
            cache.set(cache_key,user,timeout=3600)
    return None