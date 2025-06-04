from app import db
from datetime import datetime
from flask_login import current_user
from app.models import Eventos,Tags, Inscricoes, Usuario
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

    favoritos = current_user.favoritos.all()

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

    return render_template("user_homepage.html", lista_eventos = lista_eventos,termo=termo, favoritos=favoritos)

def verificar_notificacoes():
    if current_user.is_authenticated:
        hoje = datetime.now().date()
        aviso_dias = 3  # Quantos dias antes avisar

        eventos_salvos = list(current_user.favoritos)
        inscricoes = (
            db.session.query(Inscricoes, Eventos)
            .join(Eventos, Inscricoes.eventos_id == Eventos.id)
            .filter(Inscricoes.usuario_id == current_user.id)
            .all()
        )

        eventos_inscritos = [evento for _, evento in inscricoes]

        eventos_a_notificar = []
        for evento in set(eventos_salvos + eventos_inscritos):
            if evento.data_execucao and 0 <= (evento.data_execucao.date() - hoje).days <= aviso_dias:
                eventos_a_notificar.append(evento)

        # Aqui você pode armazenar em g ou session
        from flask import g
        g.eventos_notificacao = eventos_a_notificar