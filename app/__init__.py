import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'authentication.login_user_session'
login_manager.session_protection = 'strong'
bcrypt = Bcrypt()
db = SQLAlchemy()


# now exists only dev, but you're able to define your own configs such as test or prod
def create_app_flask(conf_app_type):
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config', conf_app_type + '.py')
    app.config.from_pyfile(configuration)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.datings import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth)

    return app
