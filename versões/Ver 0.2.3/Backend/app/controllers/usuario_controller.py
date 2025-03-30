import os
from app.services.security import bcrypt
from app.services.database import db
from flask import current_app, redirect, render_template, request, url_for
from flask_login import current_user, logout_user
from werkzeug.utils import secure_filename

def atualizar():
    if request.method == 'GET':
        return render_template('atualizar_usu.html')
    
    elif request.method == 'POST':
        # Verifica qual campo o usuário quer atualizar
        campo = request.form.get('campo')
        novo_valor = request.form.get('novo_valor')

        if campo == 'nome':
            current_user.nome = novo_valor
        elif campo == 'email':
            # Atualiza o email
            current_user.email = novo_valor
        elif campo == 'senha':
            # Atualiza a senha (use hash para segurança)
            current_user.senha = bcrypt.generate_password_hash(novo_valor).decode("utf-8")
        else:
            return 'Campo inválido', 400

        # Salva as alterações no banco de dados
        db.session.commit()
        return redirect(url_for('home.homepage'))
    
def upload_imagem():

    file = request.files['foto_perfil']

    if file and allowed_file(file.filename):
        # Verifica se o usuário já tem uma foto de perfil
        if current_user.foto_perfil_url:
            # Caminho completo da imagem antiga
            caminho_imagem_antiga = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.foto_perfil_url.split('/')[-1])
            
            # Verifica se o arquivo existe e exclui
            if os.path.exists(caminho_imagem_antiga):
                os.remove(caminho_imagem_antiga)

        # Salva a nova imagem
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Atualiza o caminho da imagem no banco de dados
        current_user.foto_perfil_url = f"app/static/uploads/{filename}"
        db.session.commit()

        return redirect(url_for('home.homepage'))
    else:
        return 'Tipo de arquivo não permitido. Use PNG ou JPG.', 400
    
def deletar_usuario():

    # Exclui a foto de perfil do usuário, se existir
    if current_user.foto_perfil_url:
        caminho_imagem = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.foto_perfil_url.split('/')[-1])
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)

    # Exclui o usuário do banco de dados
    db.session.delete(current_user)
    db.session.commit()

    # Faz logout do usuário
    logout_user()

    # Redireciona para a homepage
    return redirect(url_for('home.homepage'))
    
#Função que verifica a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def modo_organizador():
    return render_template('creationhub.html')