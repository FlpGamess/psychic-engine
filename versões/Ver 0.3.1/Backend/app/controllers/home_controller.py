from app.models import Eventos,Tags
from flask import render_template, request
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

#Lógica para a chamada da página principal para pessoas sem login
def home():
    termo = request.args.get('q', '').strip()

    if termo:
        lista_eventos = (
            Eventos.query
            .outerjoin(Eventos.tags)  # relacionamento definido com secondary
            .options(joinedload(Eventos.tags))  # evita N+1 queries
            .filter(
                or_(
                    Eventos.titulo.ilike(f"%{termo}%"),
                    Tags.nome.ilike(f"%{termo}%")
                )
            )
            .distinct()
            .all()
        )
    else:
        lista_eventos = Eventos.query.all()
    
    return render_template("homepage.html", lista_eventos = lista_eventos,termo=termo)

#Lógica para a chamada da página principal para pessoas com login
def user_home():
    termo = request.args.get('q', '').strip()

    if termo:
        lista_eventos = (
            Eventos.query
            .outerjoin(Eventos.tags)  # relacionamento definido com secondary
            .options(joinedload(Eventos.tags))  # evita N+1 queries
            .filter(
                or_(
                    Eventos.titulo.ilike(f"%{termo}%"),
                    Tags.nome.ilike(f"%{termo}%")
                )
            )
            .distinct()
            .all()
        )
    else:
        lista_eventos = Eventos.query.all()

    return render_template("user_homepage.html", lista_eventos = lista_eventos,termo=termo)