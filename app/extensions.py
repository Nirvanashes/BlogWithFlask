from flask import session
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_mail import Mail
from app.auth.models import User
from flask_caching import Cache


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
ckeditor = CKEditor()
bootstrap = Bootstrap5()
mail = Mail()
cache = Cache()
# For adding profile images to the comment section
gravatar = Gravatar(size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


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


def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    gravatar.init_app(app)
    cache.init_app(app)