"""
Shared Flask extension instances.

Extensions are created here (not inside create_app) so models and routes can
import ``db`` without circular imports. Migrate and LoginManager are imported
inside try/except so the public homepage can run even if optional packages
fail to load in a minimal environment.
"""

from flask_sqlalchemy import SQLAlchemy

# Core ORM — required for all database operations
db = SQLAlchemy()

# Optional: database migrations (Alembic via Flask-Migrate)
try:
    from flask_migrate import Migrate
except Exception:  # pragma: no cover
    Migrate = None  # type: ignore

# Optional: session-based authentication for admin area
try:
    from flask_login import LoginManager
except Exception:  # pragma: no cover
    LoginManager = None  # type: ignore

migrate = Migrate() if Migrate else None
login_manager = LoginManager() if LoginManager else None
