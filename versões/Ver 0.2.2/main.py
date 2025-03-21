from flask import render_template, request,redirect,url_for
from flask_login import login_user,login_required,logout_user, current_user
from models import Eventos, Usuario
from config import db, bcrypt, lm, app
from datetime import datetime
import os
from werkzeug.utils import secure_filename


# Função para carregar o usuário
@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario

#Função que verifica a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

#criando uma pasta uploads caso não exista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Rota principal
@app.route("/", methods=['GET','POST'])
def homepage():
    return render_template("homepage.html")

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
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

        return redirect(url_for('homepage'))  # Redireciona para a homepage

# Rota de registro
@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        email = request.form['emailForm']
        senha = request.form['senhaForm']
        foto_perfil_url = None
        
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, foto_perfil_url = foto_perfil_url)
        db.session.add(novo_usuario)
        db.session.commit()
        
        login_user(novo_usuario)

        return redirect(url_for('homepage'))  # Redireciona para a homepage
    
@app.route("/atualizar_usu", methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('homepage'))
    
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))  # Redireciona para a homepage

# Rota para upload de imagem
@app.route('/upload_imagem', methods=['POST'])
@login_required
def upload_imagem():

    file = request.files['foto_perfil']

    if file and allowed_file(file.filename):
        # Verifica se o usuário já tem uma foto de perfil
        if current_user.foto_perfil_url:
            # Caminho completo da imagem antiga
            caminho_imagem_antiga = os.path.join(app.config['UPLOAD_FOLDER'], current_user.foto_perfil_url.split('/')[-1])
            
            # Verifica se o arquivo existe e exclui
            if os.path.exists(caminho_imagem_antiga):
                os.remove(caminho_imagem_antiga)

        # Salva a nova imagem
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Atualiza o caminho da imagem no banco de dados
        current_user.foto_perfil_url = f"uploads/{filename}"
        db.session.commit()

        return redirect(url_for('homepage'))
    else:
        return 'Tipo de arquivo não permitido. Use PNG ou JPG.', 400
    
@app.route('/deletar', methods=['GET', 'POST'])
@login_required
def deletar_usuario():

    # Exclui a foto de perfil do usuário, se existir
    if current_user.foto_perfil_url:
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], current_user.foto_perfil_url.split('/')[-1])
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)

    # Exclui o usuário do banco de dados
    db.session.delete(current_user)
    db.session.commit()

    # Faz logout do usuário
    logout_user()

    # Redireciona para a homepage
    return redirect(url_for('homepage'))

@app.route('/eventos', methods=['GET','POST'])
@login_required
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
    
        return redirect(url_for('homepage'))  # Redireciona para a página inicial após criar o evento
    
@app.route('/Vereventos', methods=['GET','POST'])
@login_required
def vizualizar():
    if request.method == 'GET':
        eventos = Eventos.query.all()
        return render_template("vizualizar.html",eventos = eventos)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)