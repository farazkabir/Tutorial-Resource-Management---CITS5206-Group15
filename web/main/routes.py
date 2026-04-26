from flask import Blueprint, render_template, request

from ..models import Category, Material

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    materials = Material.query.order_by(Material.created_at.desc()).all()
    categories = Category.query.all()
    return render_template("home.html", materials=materials, categories=categories)


@main_bp.route("/materials")
def materials():
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
        selected_category_id=category_id
    )

@main_bp.route("/materials/<int:material_id>")
def view_material(material_id):
    material = Material.query.get_or_404(material_id)
    return render_template("view_material.html", material=material)
