from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy   
from flask_bcrypt import Bcrypt

app= Flask(__name__)
app.secret_key = 'receba'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jensen947@localhost:5432/gestao_eventos'
app.config['UPLOAD_FOLDER'] = 'static/uploads' #pasta que salva as imagens
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'} #tipos de img permitidas

lm = LoginManager(app)
lm.login_view = 'login'

db = SQLAlchemy() 
db.init_app(app)

bcrypt = Bcrypt(app)  # Inicializa o Bcrypt

