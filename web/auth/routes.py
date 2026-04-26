from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
import re

from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__, template_folder="../templates")


def valid_password(password):
    return (
        len(password) >= 6
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("admin.dashboard"))

        flash("Invalid credentials", "error")

    return render_template("login.html")


@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not current_user.check_password(current_password):
            return render_template(
                "change_password.html",
                current_error="Current password is incorrect."
            )

        if new_password != confirm_password:
            return render_template(
                "change_password.html",
                confirm_error="New passwords do not match."
            )

        if not valid_password(new_password):
            return render_template(
                "change_password.html",
                new_error="Password must be at least 6 characters and include one uppercase and one lowercase letter."
            )

        current_user.set_password(new_password)
        db.session.commit()

        flash("Password changed successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("change_password.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))