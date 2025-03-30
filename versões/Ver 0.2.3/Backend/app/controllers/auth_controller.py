from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from app.models import Usuario
from app.services.security import bcrypt
from app.services.database import db

#Lógica de login
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        email = request.form['emailForm']
        senha = request.form['senhaForm']
        user = db.session.query(Usuario).filter_by(email=email).first()
        if bcrypt.check_password_hash(user.senha, senha):
            login_user(user)

        else:
            return 'Email ou Senha incorretos'

        return redirect(url_for('home.homepage'))  # Redireciona para a homepage

#Lógica de registro
def registrar():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        email = request.form['emailForm']

        if verificar_email(email):
            return 'Email já cadastrado'

        senha = request.form['senhaForm']
        foto_perfil_url = None
        
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, foto_perfil_url = foto_perfil_url)
        db.session.add(novo_usuario)
        db.session.commit()
        
        login_user(novo_usuario)

        return redirect(url_for('home.homepage'))  # Redireciona para a homepage
    
def logout():
    logout_user()
    return redirect(url_for('home.homepage'))  # Redireciona para a homepage

def verificar_email(email):                     # Função para verifica se o email já foi cadastrado;
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario != None:
        return True