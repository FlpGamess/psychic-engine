from config import db, bcrypt
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


class Eventos(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    data_inscricao = db.Column(db.String(255))
    data_prazo = db.Column(db.String(255))
    data_execucao = db.Column(db.String(255))
    localizacao = db.Column(db.String(255)) 
    descricao = db.Column(db.String(255))  
    criador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __init__(self, titulo, data_inscricao,data_prazo,data_execucao,localizacao,descricao,criador):
        self.titulo = titulo
        self.data_inscricao = data_inscricao
        self.data_execucao = data_execucao
        self.data_prazo = data_prazo
        self.localizacao = localizacao
        self.descricao = descricao
        self.criador = criador
    