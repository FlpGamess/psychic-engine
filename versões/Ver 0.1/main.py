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