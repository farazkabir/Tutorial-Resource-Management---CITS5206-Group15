from flask import Flask
import os

from .config import Config
from .extensions import db, login_manager, migrate


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # Ensure instance folder exists for sqlite:///instance/*.db
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    # Keep migrate/login optional for "just view home.html"
    if migrate is not None:
        migrate.init_app(app, db)

    if login_manager is not None:
        login_manager.init_app(app)
        login_manager.login_view = "auth.login"

    from . import models  # noqa: F401

    # Always register main (home page)
    from .main.routes import main_bp

    app.register_blueprint(main_bp)

    # Register admin/auth only if Flask-Login is installed/initialized
    if login_manager is not None:
        from .auth.routes import auth_bp
        from .admin.routes import admin_bp

        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(admin_bp, url_prefix="/admin")

    return app

