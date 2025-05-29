from datetime import date
from flask import redirect, render_template, url_for,flash
from flask_login import current_user
from app.services.database import db
from app.models import Eventos, Usuario, Inscricoes

def inscrever_evento(evento_id):
    usuario_id = current_user.id
    evento = Eventos.query.get(evento_id)


    # Se limite for None, 0, ou vazio, considera ilimitado
    if evento.limite and evento.limite > 0:
        total_inscritos = Inscricoes.query.filter_by(eventos_id=evento_id).count()
        if total_inscritos >= evento.limite:
            flash('Limite de inscrições atingido.', 'warning')
            return redirect(url_for('evento.visualizar_route', id=evento_id))

    # Verifica se já está inscrito, se quiser
    inscrito = Inscricoes.query.filter_by(usuario_id=usuario_id, eventos_id=evento_id).first()
    
    if inscrito:
        flash("Você já está inscrito neste evento.")
        return redirect(url_for('evento.visualizar_route', id=evento_id))

    nova_inscricao = Inscricoes(
        usuario_id=usuario_id,
        eventos_id=evento_id,
        data_inscricao = date.today(),
        status='confirmado'
        
    )
    db.session.add(nova_inscricao)
    db.session.commit()
    
    flash("Inscrição realizada com sucesso!")
    return redirect(url_for('evento.visualizar_route', id=evento_id))

def visualizar_inscricoes_usuario():
    usuario_id = current_user.id

    inscricoes = (
        db.session.query(Inscricoes, Eventos,Usuario)
        .join(Eventos, Inscricoes.eventos_id == Eventos.id)
        .join(Usuario, Eventos.criador == Usuario.id)
        .filter(Inscricoes.usuario_id == usuario_id)
        .all()
    )

    return render_template('minhas_inscricoes.html', inscricoes=inscricoes)

def visualizar_inscritos_evento(evento_id):
    id = evento_id

    inscritos = (
        db.session.query(Usuario.id, Usuario.nome)
        .select_from(Usuario)
        .join(Inscricoes, Usuario.id == Inscricoes.usuario_id)
        .filter(Inscricoes.eventos_id == id)
        .all()
    )

    return render_template('inscritos.html', inscritos = inscritos)