from flask import Flask
from config import Config
from extensions import db, login_manager, init_extensions
from model import User
from auth import auth_bp
from blog import blog_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return db.get_or_404(User, user_id)

    return app
