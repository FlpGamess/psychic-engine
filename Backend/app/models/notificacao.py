from app import db

class Notificacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    eventos_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    mensagem = db.Column(db.String(1000))
    data_envio = db.Column(db.DateTime)

    usuario = db.relationship('Usuario', backref='notificacoes')
    evento = db.relationship('Eventos', backref='notificacoes')

    def Notificacao(self,usuario_id, evento_id, mensagem, data_envio):
        self.usuario_id = usuario_id
        self.evento_id = evento_id
        self.mensagem = mensagem
        self.data_envio = data_envio
