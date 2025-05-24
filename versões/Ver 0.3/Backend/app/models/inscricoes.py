from app import db

from datetime import date

class Inscricoes(db.Model):
    __tablename__ = 'inscricao'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    eventos_id = db.Column(db.Integer, nullable=False)
    compareceu = db.Column(db.Boolean, default=False)
    data_inscricao = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(10), nullable=False)

    def __init__(self, usuario_id, eventos_id, status, compareceu=False, data_inscricao=None):
        self.usuario_id = usuario_id
        self.eventos_id = eventos_id
        self.status = status
        self.compareceu = compareceu
        self.data_inscricao = data_inscricao if data_inscricao else date.today()

    