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
                <td>PC-0.1-01</td>
                <td>Sistema de Login e Botões</td>
                <td>Compilado</td>
                <td>09/03/2025</td>
            </tr>
        </tbody>
    </table>
</div>

### 1. Geral
Foi criado o arquivo **Db.py** sendo um script que reverencia ao SQLAlchemy
Foi criado o arquivo **models.py** sendo um script que guarda as classes do programa que serão usadas para a manipulação do banco de dados
Foi criado o **main.py** responsável pelas rotas, conexão com o banco de dados, etc
Foi criado o **homepage.html** sendo a pagina principal do programa quando o usuário acessar a aplicação variando se o usuário estiver ou não logado
Foi criado o **atualizar_usu.html** sendo responsável por atualizar informações do usuário no banco como troca de email, senha etc.
Foi criado o **login.html responsável** pelo login do usuário e acesso ao site
Foi criado o **register.html** responsável por registrar o usuário no banco de dados e consequentemente enviar o login para o banco.
No **main.py** foram criadas as rotas de login,registrar,homepage,logout e atualizar_usu respectivamente responsaveis por: login, registro, pagina inicial, logout e atualização das informações do usuario
Foram criados botões no html responsaveis por direcionar o usuario para um novo html
---

### 2. Programação

**Db.py**

Foi importado a biblioteca fask_sqlalchemy para a conexão do banco de dados, a variável db recebe o modelo do SQLAlchemy a fazendo ter todas as propriedades para manipulação de um banco:
```Python
from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()


```

**models.py**

Foi importada a variável db do arquivo Db.py, após isso é criada a classe Usuario recebendo o modelo de classe para banco de dados, ela reverencia a tabelo usuários tendo seus componentes o id,nome,email,senha e foto_perfil_url.

```Python
from db import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    foto_perfil_url = db.Column(db.String(255))

```

**main.py**

Este arquivo é responsável por controlar as rotas, conexões, tudo no programa, ele é o que conecta o backend com frontend
Foi importada a biblioteca flask responsável por redirecionar as rotas do programa com backend, request que recebe os valores do front e passa pro back, o redirect que redireciona as rotas e o url_for que redireciona as rotas através das funções.
Foi importada a bibliote flask_login responsável por toda a gestão do login, manter o usuário conectado, deslogar o usuário e reverenciar o usuário atual no programa.
É importada do arquivo models.py a classe Usuario
É importada do arquivo bd.py a variável db.
A variável app recebe o nome do banco, app_secret_key recebe uma chave para permitir que o login seja feito (esta chave é obrigatória e pode ser qualquer coisa)
O app.config chama o URI do banco e se conecta com ele e após isto o bd é iniciado na linha abaixo

A função user_loader é responsável por fazer o login do usuário a partir do id recebido e retornando o usuário atual fazendo com que o login continue até ser deslogado.
A função homepage é responsável por chamar a pagina principal do programa
A função login ela tem 2 estados:
	Caso o método chamado seja GET ela irá chamar o login.html
	Caso o método chamado seja POST ela irá receber as informações digitadas no login.html pelo usuário e caso corresponda ira logar pela funsão login_user e redirecionar para o homepage, caso alguma informação de login esteja errada o programa retornara uma mensagem de avisando:“Email ou senha incorretos”
A função registrar ela tem 2 estados:
	Caso o método chamado seja GET ele irá chamar o register.html
	Caso o método chamado seja POST ele irá receber as informações digitadas no register.html pelo usuário e armazenar no banco de dados através da manipulação de objetos com a classe Usuario e chamara a função login_user, efetuando o login e redirecionando para a homepage

A função atualizar tem 2 estados:
	Caso o método chamado seja GET ele ira chamar o atualizar_usu.html
	Caso o método chamado seja POST ele ia pegar a informação digitada pelo usuário e alterar no banco de dados sendo possível realizar uma atualização por vez.

A função Logout encerra o login do usuário e encaminha para o homepage

Este ultimo condicionamento com if __name__ serve para caso não exista um bd no ambiente ele cria e é um dos argumentos básicos para um programa Flask



```Python
from flask import Flask, render_template, request,redirect,url_for
from flask_login import LoginManager,login_user,login_required,logout_user, current_user
from models import Usuario
from db import db

app= Flask(__name__)
app.secret_key = 'receba'
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:n0r1@localhost:5432/eventos'
db.init_app(app)

# Função para carregar o usuário
@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario


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
Foi feito a homepage  tendo uma condicional que se current_user estiver logado ele mostrara um icone de perfil no canto superior direito (imagem na pasta static) e o nome de quem logou com 2 botões para logout e atualizar as informações do usuarios, se não a homepage mostrara que a pessoa não esta logada e apresentara botões para ela ir para os htmls de login ou registro

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
        .logout-button, .login-button, .register-button {
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #ff4d4d;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .logout-button:hover, .login-button:hover, .register-button:hover {
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
     <img src="{{ url_for('static', filename='user-icon.jpeg') }}" alt="Ícone do Usuário" class="user-icon">
    <div class="container">
        <h1>Bem-vindo à Minha Página, {{ current_user.nome }}!</h1>
        <p>Esta é uma página HTML básica.</p>
        <p>Você pode personalizar o conteúdo e o estilo conforme necessário.</p>
        <!-- Botão de Logout -->
        <form action="{{ url_for('logout') }}" method="post">
            <button type="submit" class="logout-button">Logout</button>
        </form>
    </a>
    <!-- Botão de Registrar -->
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
