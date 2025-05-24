from flask import Blueprint
from flask_login import current_user
from app.controllers.home_controller import home, user_home

home_bp = Blueprint('home', __name__)

# Rota principal
@home_bp.route("/", methods=['GET','POST'])
def homepage():
    if current_user.is_authenticated:
        return user_home()
    else:
        return home()
