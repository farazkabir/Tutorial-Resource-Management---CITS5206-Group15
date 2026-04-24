from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    materials = db.relationship("Material", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")
    video_url = db.Column(db.String(500), default="")
    document_url = db.Column(db.String(500), default="")
    thumbnail = db.Column(db.String(500), default="")
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
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
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
        return self.original_name.lower().endswith(".pdf")

    @property
    def is_image(self):
        return any(
            self.original_name.lower().endswith(ext)
            for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp")
        )

    @property
    def is_video(self):
        return any(
            self.original_name.lower().endswith(ext)
            for ext in (".mp4", ".webm", ".mov", ".avi")
        )
