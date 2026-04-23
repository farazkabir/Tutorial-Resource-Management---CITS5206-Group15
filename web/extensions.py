from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Optional extensions (so you can run home page without them)
try:
    from flask_migrate import Migrate
except Exception:  # pragma: no cover
    Migrate = None  # type: ignore

try:
    from flask_login import LoginManager
except Exception:  # pragma: no cover
    LoginManager = None  # type: ignore

migrate = Migrate() if Migrate else None
login_manager = LoginManager() if LoginManager else None

