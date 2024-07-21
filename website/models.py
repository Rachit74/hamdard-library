from . import db

class File(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    file_name = db.Column(db.String(200))
    file_path = db.Column(db.String(50))
    dept = db.Column(db.String(100))
