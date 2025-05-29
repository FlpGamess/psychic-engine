from app import db

evento_tags  = db.Table('evento_tags',
    db.Column('eventos_id', db.Integer, db.ForeignKey('eventos.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)