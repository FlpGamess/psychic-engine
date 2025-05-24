from app.models.eventos import Eventos
from flask import render_template, request

#Lógica para a chamada da página principal para pessoas sem login
def home():
    termo = request.args.get('q', '').strip()

    if termo:
        lista_eventos = Eventos.query.filter(Eventos.titulo.ilike(f"%{termo}%")).all()
    else:
        lista_eventos = Eventos.query.all()
    
    return render_template("homepage.html", lista_eventos = lista_eventos,termo=termo)

#Lógica para a chamada da página principal para pessoas com login
def user_home():
    termo = request.args.get('q', '').strip()

    if termo:
        lista_eventos = Eventos.query.filter(Eventos.titulo.ilike(f"%{termo}%")).all()
    else:
        lista_eventos = Eventos.query.all()

    return render_template("user_homepage.html", lista_eventos = lista_eventos,termo=termo)