from flask import Blueprint
from flask_login import login_required
from app.controllers.evento_controller import criar, visualizar

evento_bp = Blueprint('evento', __name__, url_prefix='/evento')

@evento_bp.route('/eventos', methods=['GET','POST'])
@login_required
def criar_route():
    return criar()

@evento_bp.route('/Vereventos', methods=['GET'])
@login_required
def visualizar_route():
    return visualizar()