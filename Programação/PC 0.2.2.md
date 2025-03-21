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
                <td>PC-0.2-02</td>
                <td>Criar/Vizualizar Eventos/Criptografia de senha</td>
                <td>Compilado</td>
                <td>20/03/2025</td>
            </tr>
        </tbody>
    </table>
</div>

### 1. Geral
O arquivo **models.py** recebeu os metodos construtores de classe. Em usuários o método construtor recebe a senha e criptografa em um código hash.

O arquivo **main.py** recebeu novas rotas chamadas /eventos e /Vereventos referente a função Criar e Vizualizar eventos, além de ter a rota login alterada para verificar o código hash da senha digitada e compara-la com a armazenada no banco.

O arquivo **homepage.html** recebeu novos botões para chamar estas funções, e ao apertar o botão direciona para a tela de criação e listagem de eventos respectivamente

### 2. Programação

Mudanças feitas em **model.py** com a adição dos métodos construtores de classe:
```Python
from config import db, bcrypt
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    foto_perfil_url = db.Column(db.String(255))

    def __init__(self,nome,email,senha,foto_perfil_url):
        self.nome = nome
        self.email = email
        self.senha = bcrypt.generate_password_hash(senha).decode("UTF-8")
        self.foto_perfil_url = foto_perfil_url


class Eventos(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    data_inscricao = db.Column(db.String(255))
    data_prazo = db.Column(db.String(255))
    data_execucao = db.Column(db.String(255))
    localizacao = db.Column(db.String(255)) 
    descricao = db.Column(db.String(255))  
    criador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __init__(self, titulo, data_inscricao,data_prazo,data_execucao,localizacao,descricao,criador):
        self.titulo = titulo
        self.data_inscricao = data_inscricao
        self.data_execucao = data_execucao
        self.data_prazo = data_prazo
        self.localizacao = localizacao
        self.descricao = descricao
        self.criador = criador
```

**main.py**
Adição do verificador de criptografia:
```Python
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
```

foram adicionadas as rotas /eventos  e que realiza requisições GET e POST, ao chamar a função "criar" onde irá receber os campos inseridos no html e grava-las no banco de dados
```Python
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
    
```

Também foi adicionado a rota /Vereventos que permite ver a lista de eventos criados por todos os usuários;
```Python
@app.route('/Vereventos', methods=['GET','POST'])
@login_required
def vizualizar():
    if request.method == 'GET':
        eventos = Eventos.query.all()
        return render_template("vizualizar.html",eventos = eventos)
    
```

**homepage.html**
Foi adicionado um botão de criar eventos e vizualizar eventos.
linhas adicionadas:32 á 39, 41 á 48

Criar eventos:
```HTML
<div class="button">
        <a>
            <!-- Botão para redirecionar para a pagina de criar eventos -->
            <form action="{{ url_for('criar') }}" method="get">
                <button type="submit" class="evento-button">Criar Novo Evento</button>
            </form>
        </a>
    </div>
```
Vizualizar eventos:
```HTML
<div class="button">
        <a>
            <!-- Botão para redirecionar para a pagina de criar eventos -->
            <form action="{{ url_for('vizualizar') }}" method="get">
                <button type="submit" class="evento-button">vizualizar Eventos</button>
            </form>
        </a>
    </div>
```

Foram adicionados os respectivos arquivos html de cada redirecionamento por botão:
Criar.html:
```HTML
<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}"> <!-- Linking the CSS file -->
        <script src="{{ url_for('static', filename='js/script.js') }}" defer></script> <!-- Linking the JS file -->
        <title>Eventos</title>
    </head>

    <body>
        <h1>Criar Novo Evento</h1>
    
        <form action="{{ url_for('criar') }}" method="post">
            <!-- Campo para o título do evento -->
            <div>
                <label for="tituloForm">Título do Evento:</label>
                <input type="text" id="tituloForm" name="tituloForm" placeholder="Digite o título do evento" required>
            </div>
    
            <!-- Campo para a data de início das inscrições -->
            <div>
                <label for="dataInscForm">Data de Início das Inscrições:</label>
                <input type="date" id="dataInscForm" name="dataInscForm" required>
            </div>
    
            <!-- Campo para a data limite das inscrições -->
            <div>
                <label for="dataPrazoForm">Data Limite das Inscrições:</label>
                <input type="date" id="dataPrazoForm" name="dataPrazoForm" required>
            </div>
    
            <!-- Campo para a data do evento -->
            <div>
                <label for="dataEventoForm">Data do Evento:</label>
                <input type="date" id="dataEventoForm" name="dataEventoForm" required>
            </div>
    
            <!-- Campo para a localização do evento -->
            <div>
                <label for="localizacaoForm">Localização:</label>
                <input type="text" id="localizacaoForm" name="localizacaoForm" placeholder="Digite o local do evento" required>
            </div>
    
            <!-- Campo para a descrição do evento -->
            <div>
                <label for="descricaoForm">Descrição:</label>
                <textarea id="descricaoForm" name="descricaoForm" placeholder="Descreva o evento" required></textarea>
            </div>
    
            <!-- Botão de envio -->
            <div>
                <button type="submit">Criar Evento</button>
            </div>
        </form>
    
        <!-- Link para voltar à página inicial -->
        <div>
            <a href="{{ url_for('homepage') }}">Voltar à Página Inicial</a>
        </div>
    </body>
</html>
```

Vizualizar.html:
```HTML
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}"> <!-- Linking the CSS file -->
    <script src="{{ url_for('static', filename='js/script.js') }}" defer></script> <!-- Linking the JS file -->
    <title>Tabela de Eventos</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
</head>
<body>
    <h1>Tabela de Eventos</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Título</th>
                <th>Data de Inscrição</th>
                <th>Data de Prazo</th>
                <th>Data de Execução</th>
                <th>Localização</th>
                <th>Descrição</th>
                <th>Criador</th>
            </tr>
        </thead>
        <tbody>
            {% for evento in eventos %}
            <tr>
                <td>{{ evento.id }}</td>
                <td>{{ evento.titulo }}</td>
                <td>{{ evento.data_inscricao }}</td>
                <td>{{ evento.data_prazo }}</td>
                <td>{{ evento.data_execucao }}</td>
                <td>{{ evento.localizacao }}</td>
                <td>{{ evento.descricao }}</td>
                <td>{{ evento.criador }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```
Opcionalmente uma pasta denominada config.py foi feita juntando alguns imports e incorporando o arquivo db.py de versões anteriores.
```Python
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy   
from flask_bcrypt import Bcrypt

app= Flask(__name__)
app.secret_key = 'receba'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jensen947@localhost:5432/gestao_eventos'
app.config['UPLOAD_FOLDER'] = 'static/uploads' #pasta que salva as imagens
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'} #tipos de img permitidas

lm = LoginManager(app)
lm.login_view = 'login'

db = SQLAlchemy() 
db.init_app(app)

bcrypt = Bcrypt(app)  # Inicializa o Bcrypt


```
Portanto em main.py os imports ficam da seguinte forma:
```Python
from flask import render_template, request,redirect,url_for
from flask_login import login_user,login_required,logout_user, current_user
from models import Eventos, Usuario
from config import db, bcrypt, lm, app
from datetime import datetime
import os
from werkzeug.utils import secure_filename
```

### 3. Autores
Pedro Alves
