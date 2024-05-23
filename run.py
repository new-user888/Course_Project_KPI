from app import create_app_flask, db
from app.auth.models import User

if __name__ == '__main__':
    flask_app = create_app_flask('dev')
    with flask_app.app_context():
        db.create_all()
        if not User.query.filter_by(user_name='Oleg').first:
            User.create_user(user='Oleg',
                             bio='Hello, my name is Oleg',
                             private='Im young',
                             password='password')
    flask_app.run()
