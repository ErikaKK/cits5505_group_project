from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from app.models import db, User


migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Return the user object for the given user_id
        return User.query.get(int(user_id))

    with app.app_context():
        # Register blueprints
        from . import auth, main

        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)

    return app
