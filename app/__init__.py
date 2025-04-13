from flask import Flask
from config import Config
from app.extensions import db, login_manager, init_extensions
from app.auth.models import User
from app.blog.models import BlogPost,Comment
from app.auth.routes import auth_bp
from app.blog.routes import blog_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    with app.app_context():
        db.create_all()

    return app
