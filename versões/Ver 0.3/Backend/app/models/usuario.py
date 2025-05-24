from app import db, bcrypt
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    foto_perfil_url = db.Column(db.String(255))

    def __init__(self,nome,email,senha,foto_perfil_url):
        self.nome = nome
        self.email = email
        self.senha = bcrypt.generate_password_hash(senha).decode("UTF-8")
        self.foto_perfil_url = foto_perfil_url