from flask import Blueprint

auth = Blueprint('authentication', __name__, template_folder='templates')

from app.auth import routes
