"""
SQLAlchemy database models.

Entity overview:
    User       — admin accounts (password hashing via Werkzeug)
    Category   — tutorial groupings (slug used in forms and URLs)
    Material   — a single tutorial (text, video URL, document URL, attachments)
    Attachment — files uploaded alongside a Material (PDF, image, video)
"""

from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class User(UserMixin, db.Model):
    """Administrator who can log in and manage tutorials."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password: str) -> None:
        """Hash and store a plaintext password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Return True if password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    """Groups tutorials (e.g. WordPress Basics, Elementor)."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    materials = db.relationship("Material", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Material(db.Model):
    """
    A tutorial resource shown on the public site.

    media_type drives which fields are emphasised in the admin form:
    text, video, document, or combinations with file attachments.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")  # HTML from Quill editor
    video_url = db.Column(db.String(500), default="")  # YouTube or direct URL
    document_url = db.Column(db.String(500), default="")  # External doc link
    thumbnail = db.Column(db.String(500), default="")  # Filename in uploads/
    media_type = db.Column(db.String(50), default="text")
    is_published = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    attachments = db.relationship(
        "Attachment", backref="material", lazy=True, cascade="all, delete-orphan"
    )


class Attachment(db.Model):
    """File linked to a Material (stored on disk under static/uploads/)."""

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)  # UUID-based stored name
    original_name = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(50), default="other")
    material_id = db.Column(
        db.Integer, db.ForeignKey("material.id"), nullable=False
    )
    uploaded_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    @property
    def is_pdf(self):
        """True if the original filename has a .pdf extension."""
        return self.original_name.lower().endswith(".pdf")

    @property
    def is_image(self):
        """True if the original filename is a common image type."""
        return any(
            self.original_name.lower().endswith(ext)
            for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp")
        )

    @property
    def is_video(self):
        """True if the original filename is a common video type."""
        return any(
            self.original_name.lower().endswith(ext)
            for ext in (".mp4", ".webm", ".mov", ".avi")
        )
