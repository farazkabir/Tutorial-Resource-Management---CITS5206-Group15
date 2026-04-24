from flask import Blueprint, render_template

from ..models import Category, Material

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    materials = Material.query.order_by(Material.created_at.desc()).all()
    categories = Category.query.all()
    return render_template("home.html", materials=materials, categories=categories)


@main_bp.route("/materials")
def materials():
    materials = Material.query.order_by(Material.created_at.desc()).all()
    categories = Category.query.all()
    return render_template("home.html", materials=materials, categories=categories)


@main_bp.route("/materials/<int:material_id>")
def view_material(material_id):
    material = Material.query.get_or_404(material_id)
    return render_template("view_material.html", material=material)

@main_bp.route("/category/<slug>")
def category_page(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()

    materials = (
        Material.query
        .filter_by(category_id=category.id)
        .order_by(Material.created_at.desc())
        .all()
    )

    categories = Category.query.all()

    return render_template(
        "category.html",
        category=category,
        materials=materials,
        categories=categories
    )
