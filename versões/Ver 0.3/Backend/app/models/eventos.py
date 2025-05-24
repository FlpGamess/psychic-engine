from app import db

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
    foto_evento_url = db.Column(db.String(255))

    def __init__(self, titulo, data_inscricao,data_prazo,data_execucao,localizacao,descricao,criador,foto_evento_url):
        self.titulo = titulo
        self.data_inscricao = data_inscricao
        self.data_execucao = data_execucao
        self.data_prazo = data_prazo
        self.localizacao = localizacao
        self.descricao = descricao
        self.criador = criador
        self.foto_evento_url = foto_evento_url
    