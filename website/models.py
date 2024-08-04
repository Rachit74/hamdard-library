from . import db

class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))
    email = db.Column(db.String(200))
    user_admin = db.Column(db.Boolean(), default=False)
    user_super_admin = db.Column(db.Boolean(), default=False)

        # Flask-Login requires these methods
    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True  # Change this as needed based on your user status

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
    def is_admin(self):
        return bool(self.user_admin)
    
    def is_super_admin(self):
        return bool(self.user_super_admin)

class File(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    file_name = db.Column(db.String(200))
    file_path = db.Column(db.String(50))
    dept = db.Column(db.String(100))
    file_status = db.Column(db.Boolean(), default=False)

    #foreign key realtion to user model
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='files')

User.files = db.relationship('File', back_populates='user')