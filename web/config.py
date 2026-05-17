"""
Application configuration.

Values can be overridden via environment variables for production deployments.
See README.md for ``SECRET_KEY`` and ``DATABASE_URL`` usage.
"""

import os

# Project root (parent of the ``web`` package)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """Default Flask configuration for development and local testing."""

    # Session cookies and CSRF-related signing — change in production
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # SQLite file stored under instance/ when using default relative URI
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploaded thumbnails, PDFs, and videos (served from static/uploads)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "web", "static", "uploads")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB per request
