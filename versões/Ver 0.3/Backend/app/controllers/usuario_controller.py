import os
from app.controllers.image_controller import allowed_file
from app.services.security import bcrypt
from app.services.database import db
from flask import current_app, redirect, render_template, request, url_for
from flask_login import current_user, logout_user
from werkzeug.utils import secure_filename

from app.models.usuario import Usuario

def atualizar():
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    
    if request.method == 'GET':
        return render_template('atualizar_usu.html')
    
    elif request.method == 'POST':

        novo_nome = request.form['nomeForm']
        novo_email = request.form['emailForm']
        nova_senha = request.form['senhaForm']

        # Se os campos estiverem vazio
        if not novo_nome.strip() and not novo_email.strip() and not nova_senha.strip():
            return render_template('atualizar_usu.html', mensagem='Os campos não podem estar vazios.')

        if novo_nome:
            usuario.nome = novo_nome
        if novo_email:
            usuario.email = novo_email
        if nova_senha:
            usuario.senha = bcrypt.generate_password_hash(nova_senha).decode("utf-8")

        # Salva as alterações no banco de dados
        db.session.commit()
        return redirect(url_for('usuario.perfil_route'))
    
def upload_imagem_perfil():
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
        current_user.foto_perfil_url = f"uploads/{filename}"
        db.session.commit()

        return redirect(url_for('usuario.perfil_route'))
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

def modo_organizador():
    return render_template('creationhub.html')

def perfil():
    return render_template('perfil.html')