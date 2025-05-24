from datetime import date
from flask import redirect, render_template, url_for,flash
from flask_login import current_user
from app.services.database import db
from app.models import Eventos, Usuario, Inscricoes

def inscrever_evento(evento_id):
    usuario_id = current_user.id
    status = 'confirmado'

    # Verifica se já está inscrito, se quiser
    inscrito = Inscricoes.query.filter_by(usuario_id=usuario_id, eventos_id=evento_id).first()
    
    if inscrito:
        flash("Você já está inscrito neste evento.")
        return redirect(url_for('home.homepage'))

    nova_inscricao = Inscricoes(
        usuario_id=usuario_id,
        eventos_id=evento_id,
        data_inscricao = date.today(),
        status=status
        
    )
    db.session.add(nova_inscricao)
    db.session.commit()
    
    flash("Inscrição realizada com sucesso!")
    return redirect(url_for('home.homepage'))

def visualizar_inscricoes_usuario():
    usuario_id = current_user.id

    inscricoes = (
        db.session.query(Inscricoes, Eventos)
        .join(Eventos, Inscricoes.eventos_id == Eventos.id)
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
