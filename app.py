from flask import Flask, render_template
from models import db, Material
from auth_routes import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///materials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(auth_bp, url_prefix="/auth")

db.init_app(app)

# Home page
@app.route('/')
def home():
    materials = Material.query.all()
    return render_template("home.html", materials=materials)

# Login page
@app.route('/login')
def login():
    return render_template("login.html")

# Admin page
@app.route('/admin/materials')
def admin_materials():
    materials = Material.query.all()
    return render_template("admin_materials.html", materials=materials)

# View material
@app.route('/materials/<int:id>')
def view_material(id):
    material = Material.query.get(id)
    return render_template("view_material.html", material=material)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
