from flask import Flask, render_template, redirect, url_for, session
from models import db, Material
from auth_routes import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///materials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

db.init_app(app)
app.register_blueprint(auth_bp)


def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# Home page
@app.route('/')
def home():
    materials = Material.query.all()
    return render_template("home.html", materials=materials)


# Admin page
@app.route('/admin/materials')
@login_required
def admin_materials():
    materials = Material.query.all()
    return render_template("admin_materials.html", materials=materials)


# View material
@app.route('/materials/<int:id>')
def view_material(id):
    material = Material.query.get_or_404(id)
    return render_template("view_material.html", material=material)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
