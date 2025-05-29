from flask import Blueprint
from flask_login import login_required
from app.controllers.auth_controller import login, logout, registrar

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rota de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login_route():
    return login()

# Rota de registrar
@auth_bp.route('/registrar', methods=['GET', 'POST'])
def registrar_route():
    return registrar()

# Rota de logout
@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout_route():
    return logout()