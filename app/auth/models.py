from app import db, bcrypt
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), unique=True)
    user_bio = db.Column(db.String(100))
    user_private = db.Column(db.String(100))
    user_password = db.Column(db.String(80))

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    @classmethod
    def create_user(cls, user, bio, private, password):
        user = cls(user_name=user,
                   user_bio=bio,
                   user_private=private,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8')
                   )
        db.session.add(user)
        db.session.commit()
        return user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
