from flask_login import UserMixin
from firebase_admin import firestore

db = firestore.client()

class User(UserMixin):
    def __init__(self, uid: str, username: str, email: str, password: str, is_admin: bool, is_super_admin: bool):
        self.id = uid
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_super_admin = is_super_admin

    @staticmethod
    def get_user(user_id: str):
        ref = db.collection('users').document(user_id)
        ref_ = ref.get()
        if ref_.exists:
            data = ref_.to_dict()
            return User(user_id, data['username'], data['email'], data['password'], data['is_admin'], data['is_super_admin'])
        return None
    
    def is_super_admin(self):
        return self.is_super_admin
