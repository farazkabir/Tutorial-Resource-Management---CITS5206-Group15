"""
Public-facing routes (no login required).

Blueprint: ``main``
Endpoints: home page, filterable materials list, single tutorial view.
"""

from flask import Blueprint, render_template, request

from ..models import Category, Material

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """
    Landing page — hero section and latest tutorials.

    Returns:
        Rendered home.html with all materials and categories.
    """
    materials = Material.query.order_by(Material.created_at.desc()).all()
    categories = Category.query.all()
    return render_template("home.html", materials=materials, categories=categories)


@main_bp.route("/materials")
def materials():
    """
    Browse tutorials with optional category filter.

    Query params:
        category_id (int, optional): Filter by Category.id.

    Returns:
        Rendered materials.html with filtered list and category pills.
    """
    category_id = request.args.get("category_id", type=int)

    query = Material.query

    if category_id:
        query = query.filter(Material.category_id == category_id)

    materials = query.order_by(Material.created_at.desc()).all()
    categories = Category.query.all()

    return render_template(
        "materials.html",
        materials=materials,
        categories=categories,
        selected_category_id=category_id,
    )


@main_bp.route("/materials/<int:material_id>")
def view_material(material_id):
    """
    Display a single tutorial (rich text, YouTube embed, PDFs, document link).

    Args:
        material_id: Primary key of the Material row.

    Returns:
        404 if not found; otherwise view_material.html.
    """
    material = Material.query.get_or_404(material_id)
    return render_template("view_material.html", material=material)
