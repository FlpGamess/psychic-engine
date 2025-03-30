from flask import Blueprint
from flask_login import login_required
from app.controllers.usuario_controller import atualizar, upload_imagem, deletar_usuario, modo_organizador


usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')
@usuario_bp.route("/atualizar_usu", methods=['GET', 'POST'])
@login_required
def atualizar_route():
    return atualizar()

# Rota para upload de imagem
@usuario_bp.route('/upload_imagem', methods=['POST'])
@login_required
def upload_imagem_route():
    return upload_imagem()

@usuario_bp.route('/deletar', methods=['GET', 'POST'])
@login_required
def deletar_usuario_route():
    return deletar_usuario()

@usuario_bp.route('/organizador', methods=['GET'])
@login_required
def organizador_route():
    return modo_organizador()