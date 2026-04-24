import os
import uuid

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import Attachment, Category, Material

admin_bp = Blueprint("admin", __name__, template_folder="../templates")

ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx",
    "png", "jpg", "jpeg", "gif", "webp",
    "mp4", "webm", "mov", "avi",
}


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_file(file) -> str | None:
    if not file or not file.filename:
        return None
    if not _allowed(file.filename):
        return None
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(upload_dir, unique_name))
    return unique_name


def _file_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    if ext == "pdf":
        return "pdf"
    if ext in ("doc", "docx"):
        return "document"
    if ext in ("png", "jpg", "jpeg", "gif", "webp"):
        return "image"
    if ext in ("mp4", "webm", "mov", "avi"):
        return "video"
    return "other"


def _remove_file(filename: str) -> None:
    if not filename:
        return
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        os.remove(path)


def _handle_attachments(mat, form_field, forced_type=None):
    """Save uploaded files from a form field as Attachment rows."""
    for f in request.files.getlist(form_field):
        saved = _save_file(f)
        if saved:
            att = Attachment(
                filename=saved,
                original_name=secure_filename(f.filename),
                file_type=forced_type or _file_type(f.filename),
                material_id=mat.id,
            )
            db.session.add(att)


# ── Dashboard (main admin page with materials list) ─────────────

@admin_bp.route("/")
@login_required
def dashboard():
    materials = Material.query.order_by(Material.created_at.desc()).all()
    return render_template("admin_dashboard.html", materials=materials)


# ── Create ───────────────────────────────────────────────────────

@admin_bp.route("/materials/create", methods=["GET", "POST"])
@login_required
def create_material():
    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("admin.create_material"))

        mat = Material(
            title=title,
            description=request.form.get("description", "").strip(),
            content=request.form.get("content", ""),
            video_url=request.form.get("video_url", "").strip(),
            document_url=request.form.get("document_url", "").strip(),
            media_type=request.form.get("media_type", "text"),
            is_published="is_published" in request.form,
            display_order=int(request.form.get("display_order", 0) or 0),
        )

        cat_slug = request.form.get("category", "")
        if cat_slug:
            cat = Category.query.filter_by(slug=cat_slug).first()
            if cat:
                mat.category = cat

        thumb = request.files.get("thumbnail")
        saved_thumb = _save_file(thumb)
        if saved_thumb:
            mat.thumbnail = saved_thumb

        db.session.add(mat)
        db.session.flush()

        _handle_attachments(mat, "pdf_files", forced_type="pdf")
        _handle_attachments(mat, "video_files")

        db.session.commit()
        flash("Tutorial created!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin_form.html", categories=categories, material=None)


# ── Edit ─────────────────────────────────────────────────────────

@admin_bp.route("/materials/<int:material_id>/edit", methods=["GET", "POST"])
@login_required
def edit_material(material_id):
    mat = Material.query.get_or_404(material_id)
    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("admin.edit_material", material_id=mat.id))

        mat.title = title
        mat.description = request.form.get("description", "").strip()
        mat.content = request.form.get("content", "")
        mat.video_url = request.form.get("video_url", "").strip()
        mat.document_url = request.form.get("document_url", "").strip()
        mat.media_type = request.form.get("media_type", "text")
        mat.is_published = "is_published" in request.form
        mat.display_order = int(request.form.get("display_order", 0) or 0)

        cat_slug = request.form.get("category", "")
        if cat_slug:
            cat = Category.query.filter_by(slug=cat_slug).first()
            mat.category = cat if cat else None
        else:
            mat.category = None

        thumb = request.files.get("thumbnail")
        saved_thumb = _save_file(thumb)
        if saved_thumb:
            _remove_file(mat.thumbnail)
            mat.thumbnail = saved_thumb

        # Remove attachments the user checked for deletion
        for att_id in request.form.getlist("delete_attachments"):
            att = Attachment.query.get(int(att_id))
            if att and att.material_id == mat.id:
                _remove_file(att.filename)
                db.session.delete(att)

        db.session.flush()

        _handle_attachments(mat, "pdf_files", forced_type="pdf")
        _handle_attachments(mat, "video_files")

        db.session.commit()
        flash("Tutorial updated!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin_form.html", categories=categories, material=mat)


# ── Delete ───────────────────────────────────────────────────────

@admin_bp.route("/materials/<int:material_id>/delete", methods=["POST"])
@login_required
def delete_material(material_id):
    mat = Material.query.get_or_404(material_id)

    _remove_file(mat.thumbnail)
    for att in mat.attachments:
        _remove_file(att.filename)

    db.session.delete(mat)
    db.session.commit()
    flash("Tutorial deleted.", "success")
    return redirect(url_for("admin.dashboard"))
