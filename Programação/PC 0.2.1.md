## Procedimento de Compilação

<!-- Aqui fica o cabeçalho, onde teremos informações rápidas sobre as modificações do procedimento-->
<div align="center">
    <table border="1">
        <thead>
            <tr>
                <th><strong>CÓDIGO</strong></th>
                <th><strong>TÍTULO</strong></th>
                <th><strong>STATUS</strong></th>
                <th><strong>DATA DA REVISÃO</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>PC-0.2-01</td>
                <td>Excluir Perfil do Usuario</td>
                <td>Em espera</td>
                <td>12/03/2025</td>
            </tr>
        </tbody>
    </table>
</div>

### 1. Geral
O arquivo **main.py** recebeu uma nova rota chamada /deletar referente a função deletar/usuario
O arquivo **homepage.html** recebeu um novo botão para chamar esta função, ele ao apertar gera uma confirmação caso o usuario queira mesmo deletar sua conta
---

### 2. Programação

**main.py**



```Python
from flask import Flask, render_template, request,redirect,url_for, render_template
from flask_login import LoginManager,login_user,login_required,logout_user, current_user
from models import Usuario
from db import db
import os 
from werkzeug.utils import secure_filename

app= Flask(__name__)
app.secret_key = 'receba'
app.config['UPLOAD_FOLDER'] = 'static/uploads' #pasta que salva as imagens
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'} #tipos de img permitidas
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:n0r1@localhost:5432/eventos'
db.init_app(app)

#criando uma pasta uloads caso não exista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Função para carregar o usuário
@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario

#Função que verifica a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Rota principal
@app.route("/", methods=['GET','POST'])
#@login_required
def homepage():
    #print(current_user.email)
    return render_template("homepage.html")


# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['emailForm']
        senha = request.form['senhaForm']
        user = db.session.query(Usuario).filter_by(email=email, senha=senha).first()

        if not user:
            return 'Email ou Senha incorretos'
        login_user(user)
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
        
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
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
            current_user.senha = novo_valor
        else:
            return 'Campo inválido', 400

        # Salva as alterações no banco de dados
        db.session.commit()
        return redirect(url_for('homepage'))
    
# Rota para upload de imagem
@app.route('/upload_imagem', methods=['POST'])
@login_required
def upload_imagem():
    if 'foto_perfil' not in request.files:
        return 'Nenhum arquivo enviado', 400

    file = request.files['foto_perfil']
    if file.filename == '':
        return 'Nenhum arquivo selecionado', 400

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

    
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))  # Redireciona para a homepage
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

**homepage.html**

foi feita uma condicional para verificar se o usuario atualmente logado possui uma uri de imagem no banco de dados e caso tenha o programa a procura e exibe na home page no lugar do icone generico,
caso nao tenha uma uri, o programa exibira um icone preto padrão.
linhas adicionadas/mudadas: 251 a 257

```HTML
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha Página</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            position: relative; /* Para posicionar o ícone */
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
        }
        .logout-button, .login-button, .register-button, .atulization-button {
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #ff4d4d;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .logout-button:hover, .login-button:hover, .register-button:hover, .atulization-button:hover {
            background-color: #cc0000;
        }
        /* Estilo do ícone */
        .user-icon {
            position: absolute; /* Posiciona o ícone */
            top: 20px; /* Distância do topo */
            right: 20px; /* Distância da direita */
            width: 40px; /* Tamanho do ícone */
            height: 40px;
            cursor: pointer; /* Cursor de ponteiro */
        }
    </style>
</head>
<body>
    {% if current_user.is_authenticated %}
  <!-- Ícone no canto superior direito -->
{% if current_user.foto_perfil_url %}
    <img src="{{ url_for('static', filename=current_user.foto_perfil_url) }}" alt="Ícone do Usuário" class="user-icon">
{% else %}
    <img src="{{ url_for('static', filename='user-icon.jpeg') }}" alt="Ícone do Usuário" class="user-icon">
{% endif %}
<div class="container">
        <h1>Bem-vindo à Minha Página, {{ current_user.nome }}!</h1>
        <p>Esta é uma página HTML básica.</p>
        <p>Você pode personalizar o conteúdo e o estilo conforme necessário.</p>

        <!-- Formulário de Upload de Imagem -->
        <form action="{{ url_for('upload_imagem') }}" method="post" enctype="multipart/form-data">
            <label for="foto_perfil">Escolha uma imagem de perfil:</label>
            <input type="file" name="foto_perfil" id="foto_perfil" accept="image/png, image/jpeg">
            <button type="submit" class="logout-button">Enviar Imagem</button>
        </form>

        <!-- Botão de Logout -->
        <form action="{{ url_for('logout') }}" method="post">
            <button type="submit" class="logout-button">Logout</button>
        </form>

        <!-- Botão de Atualizar Conta -->
        <a href="{{ url_for('atualizar') }}">
            <button type="button" class="atulization-button">Atualizar Conta</button>
        </a>
    </div>
    {% else %}
        <h1>Você não está logado, irmão.</h1>
        <!-- Botão de Login -->
        <a href="{{ url_for('login') }}">
            <button type="button" class="login-button">Login</button>
        </a>
        <!-- Botão de Registrar -->
        <a href="{{ url_for('registrar') }}">
            <button type="button" class="register-button">Registrar</button>
        </a>
    {% endif %}
</body>
</html>
```

### 3. Autores
Felipe Pereira da Silva

Vulgo FlpGamess.
