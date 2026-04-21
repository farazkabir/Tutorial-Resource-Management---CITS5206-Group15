from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Home (All Materials page)
@app.route('/')
def home():
    materials = []
    return render_template("home.html", materials=materials)

# Login page
@app.route('/login')
def login():
    return render_template("login.html")

# Admin Materials Management
@app.route('/admin/materials')
def admin_materials():
    materials = []
    return render_template("admin_materials.html", materials=materials)

# View Material page
@app.route('/materials/<int:id>')
def view_material(id):
    material = {"id": id}
    return render_template("view_material.html", material=material)

if __name__ == '__main__':
    app.run(debug=True)
