import os
from datetime import datetime
from flask import current_app,redirect, render_template, request, url_for,flash
from flask_login import current_user
from app.controllers.image_controller import allowed_file
from app.services.database import db
from werkzeug.utils import secure_filename
import uuid

from app.models.eventos import Eventos
from app.models.usuario import Usuario

def criar():
    if request.method == 'GET':
        return render_template('criar.html')
    
    elif request.method == 'POST':
        titulo = request.form['tituloForm']
        data_inscricao = datetime.strptime(request.form['dataInscForm'], '%Y-%m-%d')
        data_prazo = datetime.strptime(request.form['dataPrazoForm'], '%Y-%m-%d')
        data_execucao = datetime.strptime(request.form['dataEventoForm'], '%Y-%m-%d')    
        localizacao = request.form['localizacaoForm']
        descricao = request.form['descricaoForm']
        criador = current_user.id

        # salvando a imagem enviada
        imagem = request.files['fotoEventoForm']
        if imagem and imagem.filename != '' and allowed_file(imagem.filename):
            nome_seguro = secure_filename(imagem.filename)
            extensao = nome_seguro.rsplit('.', 1)[1]
            nome_unico = f"{uuid.uuid4().hex}.{extensao}"
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_unico)
            imagem.save(caminho)
            foto_evento_url = f"uploads/{nome_unico}"
        else:
            foto_evento_url = "default-event.png"

        novo_evento = Eventos(
            titulo=titulo,
            data_inscricao=data_inscricao,
            data_prazo=data_prazo,
            data_execucao=data_execucao,
            localizacao=localizacao,
            descricao=descricao, 
            criador=criador,
            foto_evento_url=foto_evento_url)
        
        db.session.add(novo_evento)
        db.session.commit()
    
        return redirect(url_for('home.homepage'))  # Redireciona para a página inicial após criar o evento
    
def visualizar(id):       # FUTURAMENTE SERA A FUNÇÂO DA PAGINA ESPECIFICA DE CADA EVENTO;
    if request.method == 'GET':
        evento = Eventos.query.get_or_404(id)
        criador = Usuario.query.get(evento.criador)
        return render_template("event_template.html",evento = evento, criador_nome = criador.nome)
    
def meus_eventos():
    if request.method == 'GET':
        eventos_usuario = Eventos.query.filter_by(criador=current_user.id).all()
        return render_template('visualizar.html', eventos=eventos_usuario)

def editar(id):
    evento = Eventos.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('editar.html',evento=evento)
    
    elif request.method == 'POST':
            evento.titulo = request.form['tituloForm']
            evento.data_inscricao = datetime.strptime(request.form['dataInscForm'], '%Y-%m-%d')
            evento.data_prazo = datetime.strptime(request.form['dataPrazoForm'], '%Y-%m-%d')
            evento.data_execucao = datetime.strptime(request.form['dataEventoForm'], '%Y-%m-%d')
            evento.localizacao = request.form['localizacaoForm']
            evento.descricao = request.form['descricaoForm']

            imagem = request.files['fotoEventoForm']
            if imagem and imagem.filename != '' and allowed_file(imagem.filename):
                nome_seguro = secure_filename(imagem.filename)
                extensao = nome_seguro.rsplit('.', 1)[1]
                nome_unico = f"{uuid.uuid4().hex}.{extensao}"
                caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_unico)
                imagem.save(caminho)
                evento.foto_evento_url = f"uploads/{nome_unico}"

            db.session.commit()
            flash("Evento atualizado com sucesso.", "success")
            return redirect(url_for('evento.meus_eventos_route'))
