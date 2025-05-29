from flask_login import login_required
from app.controllers.inscricoes_controller import inscrever_evento, visualizar_inscricoes_usuario ,visualizar_inscritos_evento
from flask import Blueprint


inscricoes_bp = Blueprint('inscricoes', __name__, url_prefix='/inscricoes')  # Certifique-se de ter isso

@inscricoes_bp.route('/inscrever/<int:evento_id>', methods=['POST'])
@login_required
def inscrever(evento_id):
    return inscrever_evento(evento_id)

@inscricoes_bp.route('/minscricoes', methods=['GET'])
@login_required
def minhas_inscricoes():
    return visualizar_inscricoes_usuario()

@inscricoes_bp.route('/eventinscricoes/<int:id>',methods=['GET'])
@login_required
def inscritos_evento_route(id):
    return visualizar_inscritos_evento(id)