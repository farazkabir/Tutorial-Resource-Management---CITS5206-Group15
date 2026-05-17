"""
Flask application package.

Exposes ``create_app()`` — the application factory that wires configuration,
database extensions, blueprints, and Flask-Login.
"""

import os

from flask import Flask

from .config import Config
from .extensions import db, login_manager, migrate


def create_app(config_object: type[Config] = Config) -> Flask:
    """
    Build and configure the Flask application.

    Args:
        config_object: Configuration class (default: ``Config`` from config.py).

    Returns:
        A fully configured Flask app with blueprints registered.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # SQLite database lives in instance/ when using default URI
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    # Migrate and Login are optional so the home page can run with minimal deps
    if migrate is not None:
        migrate.init_app(app, db)

    if login_manager is not None:
        login_manager.init_app(app)
        login_manager.login_view = "auth.login"

    # Import models so SQLAlchemy metadata is registered before migrations
    from . import models  # noqa: F401

    if login_manager is not None:

        @login_manager.user_loader
        def load_user(user_id: str):
            """Flask-Login callback: load User by primary key from session."""
            return models.User.query.get(int(user_id))

    # Public routes (always available)
    from .main.routes import main_bp

    app.register_blueprint(main_bp)

    # Admin and auth require Flask-Login
    if login_manager is not None:
        from .auth.routes import auth_bp
        from .admin.routes import admin_bp

        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
