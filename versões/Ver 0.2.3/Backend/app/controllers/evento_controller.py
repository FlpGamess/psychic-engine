from datetime import datetime
from flask import redirect, render_template, request, url_for
from flask_login import current_user
from app.services.database import db

from app.models.eventos import Eventos

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

        novo_evento = Eventos(
            titulo=titulo,
            data_inscricao=data_inscricao,
            data_prazo=data_prazo,
            data_execucao=data_execucao,
            localizacao=localizacao,
            descricao=descricao, 
            criador= criador)
        
        db.session.add(novo_evento)
        db.session.commit()
    
        return redirect(url_for('home.homepage'))  # Redireciona para a página inicial após criar o evento
    
def visualizar():
    if request.method == 'GET':
        eventos = Eventos.query.all()
        return render_template("visualizar.html",eventos = eventos)