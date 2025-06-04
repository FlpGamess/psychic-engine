from flask import Blueprint
from flask_login import login_required
from app.controllers.evento_controller import criar, visualizar, meus_eventos, editar, excluir, toggle_favorito

evento_bp = Blueprint('evento', __name__, url_prefix='/evento')

@evento_bp.route('/eventos', methods=['GET','POST'])
@login_required
def criar_route():
    return criar()

@evento_bp.route('/Ver_eventos/<int:id>', methods=['GET'])
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

@evento_bp.route('/deletar_evento/<int:id>',methods = ['GET' , 'POST'])
@login_required
def excluir_route(id):
    return excluir(id)

@evento_bp.route('/toggle_favorito/<int:id>', methods=['POST'])
@login_required
def toggle_favorito_route(id):
    return toggle_favorito(id)