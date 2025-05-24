from flask import Blueprint
from flask_login import login_required
from app.controllers.evento_controller import criar, visualizar, meus_eventos,editar

evento_bp = Blueprint('evento', __name__, url_prefix='/evento')

@evento_bp.route('/eventos', methods=['GET','POST'])
@login_required
def criar_route():
    return criar()

@evento_bp.route('/Ver_eventos/<int:id>', methods=['GET'])
# @login_required
def visualizar_route(id):
    return visualizar(id)

@evento_bp.route('/meus_eventos',methods=['GET'])
@login_required
def meus_eventos_route():
    return meus_eventos()

@evento_bp.route('/editar_eventos/<int:id>', methods=['GET','POST'])
@login_required
def editar_route(id):
    return editar(id)