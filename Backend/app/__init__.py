import os
from flask import Flask
from flask_login import LoginManager
from app.services import bcrypt ,db, mail
from app.models.usuario import Usuario

lm = LoginManager()
lm.login_view = 'login'

def create_app():
    app= Flask(__name__)

    #configurações do flask
    app.secret_key = 'receba'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost:5432/gestaoeventosdb'

    # Fel
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:n0r1@localhost:5432/eventos'
    
    # Configura caminho absoluto para uploads
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    
    # Cria a pasta se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'} #tipos de img permitidas


    #configurações de email:
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] =  'gab.msilva70@gmail.com'        # Coloque o gmail que deseja usar para o envio de mensagens a outros endereços
    app.config['MAIL_PASSWORD'] =  'Te$0uro08'        # Coloque a senha de aplicativo que configurou; EX: google = senha de 16 caracteres gerada;
    app.config['MAIL_DEFAULT_SENDER'] =   'gab.msilva70@gmail.com'   # Coloque o gmail que deseja usar para o envio de mensagens a outros endereços

    #configuração do scheduler
    app.config['SCHEDULER_API_ENABLED'] = True  # opcional, para habilitar painel de debug


    #inicializações
    db.init_app(app)
    bcrypt.init_app(app)
    lm.init_app(app)
    mail.init_app(app)

    from .routes import init_routes

    init_routes(app)  # Passa 'app' para registrar os Blueprints

    # Função para carregar o usuário
    @lm.user_loader
    def user_loader(id):
        usuario = db.session.query(Usuario).filter_by(id=id).first()
        return usuario

    return app