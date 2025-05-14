from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from app.models import db, User
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler


migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Set the login view
login_manager.login_message = (
    "Please log in to access this page"  # Set the login prompt message
)


def configure_logging(app):
    handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=3)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf = CSRFProtect(app)

    if config:
        app.config.update(config)
    configure_logging(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Return the user object for the given user_id
        return User.query.get(int(user_id))

    with app.app_context():
        # Register blueprints
        from . import auth, main, account, errors, messages

        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)
        app.register_blueprint(account.bp)
        app.register_blueprint(errors.bp)
        app.register_blueprint(messages.bp)
    return app
