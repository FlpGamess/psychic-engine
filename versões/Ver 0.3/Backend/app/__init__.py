import os
from flask import Flask
from flask_login import LoginManager
from app.services.security import bcrypt
from app.services.database import db

from app.models.usuario import Usuario

lm = LoginManager()
lm.login_view = 'login'

def create_app():
    app= Flask(__name__)

    #configurações do flask
    app.secret_key = 'receba'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:[senha]@localhost:5432/gestao_eventos'
    
    # Configura caminho absoluto para uploads
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    
    # Cria a pasta se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'} #tipos de img permitidas

    #inicializações
    db.init_app(app)
    bcrypt.init_app(app)
    lm.init_app(app)

    from .routes import init_routes

    init_routes(app)  # Passa 'app' para registrar os Blueprints

    # Função para carregar o usuário
    @lm.user_loader
    def user_loader(id):
        usuario = db.session.query(Usuario).filter_by(id=id).first()
        return usuario

    return app