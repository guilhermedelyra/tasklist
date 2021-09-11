from flask_login import UserMixin
from app import db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = str(id_)
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        conn = db.connect()
        user = conn.execute(f"SELECT * FROM users WHERE id = {str(user_id)}").fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        conn = db.connect()
        conn.execute(f"INSERT INTO users (id, name, email, profile_pic) VALUES ({str(id_)}, {name}, {email}, {profile_pic})")
        conn.commit()

