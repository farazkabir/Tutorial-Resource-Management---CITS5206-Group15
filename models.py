from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    material_type = db.Column(db.String(50))
    content_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
