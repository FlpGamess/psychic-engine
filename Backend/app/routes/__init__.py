from .auth import auth_bp
from .home import home_bp
from .usuario import usuario_bp
from .evento import evento_bp
from .inscricoes import inscricoes_bp
 
def init_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(home_bp)
    app.register_blueprint(usuario_bp, url_prefix='/usuario')
    app.register_blueprint(evento_bp, url_prefix='/eventos')
    app.register_blueprint(inscricoes_bp, url_prefix='/inscricoes')
