from app import db

favoritos  = db.Table('favoritos',
    db.Column('eventos_id', db.Integer, db.ForeignKey('eventos.id'), primary_key=True),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
)