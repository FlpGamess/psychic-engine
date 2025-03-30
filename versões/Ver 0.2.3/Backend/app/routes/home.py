from flask import Blueprint
from app.controllers.home_controller import home

home_bp = Blueprint('home', __name__)

# Rota principal
@home_bp.route("/", methods=['GET','POST'])
def homepage():
    return home()