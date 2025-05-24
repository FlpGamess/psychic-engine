
## Procedimento de Compilação

<!-- Aqui fica o cabeçalho, onde teremos informações rápidas sobre as modificações do procedimento-->
<div align="center">
    <table border="1">
        <thead>g
            <tr>
                <th><strong>CÓDIGO</stron></th>
                <th><strong>TÍTULO</strong></th>
                <th><strong>STATUS</strong></th>
                <th><strong>DATA DA REVISÃO</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>PC-0.3</td>
                <td>Interações fundamentais com os eventos</td>
                <td>Compilado</td>
                <td>24/05/2025</td>
            </tr>
        </tbody>
    </table>
</div>

### 1. Geral
- Os processos de criação, edição, visualização de eventos foi implementada;
- Os métodos de inscrição foram feitos;
- Usuarios não logados poderão visualizar os eventos presentes no sistema, apenas necessitando criar um login caso desejem se inscrever;
- Mecanismo de busca foi implementado, mas ainda é limitado apenas pelo filtro de nome dos eventos;


## 2. Mudanças

Começando pelos modelos, a tabela de inscrições foi construida, necessária para a lógica de intermediação entre usuários e eventos;
```Python
from app import db
from datetime import date

class Inscricoes(db.Model):
    __tablename__ = 'inscricao'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    eventos_id = db.Column(db.Integer, nullable=False)
    compareceu = db.Column(db.Boolean, default=False)
    data_inscricao = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(10), nullable=False)

    def __init__(self, usuario_id, eventos_id, status, compareceu=False, data_inscricao=None):
        self.usuario_id = usuario_id
        self.eventos_id = eventos_id
        self.status = status
        self.compareceu = compareceu
        self.data_inscricao = data_inscricao if data_inscricao else date.today()
```

As seguintes alterações foram feitas na seção de rotas:
- Em home:<br>
Foi adicionado uma verificação do estado de login do usuário, carregando funções diferentes dependendo se ele está ou não cadastrado;
```Python
# Rota principal
@home_bp.route("/", methods=['GET','POST'])
def homepage():
    if current_user.is_authenticated:
        return user_home()
    else:
        return home()
```

- Em usuario:<br>
Foi adicionado uma rota para o perfil do usuário:
```Python
@usuario_bp.route('/perfil', methods = ['GET'])
@login_required
def perfil_route():
    return perfil()
```

- Em eventos:<br>
A rota Ver_eventos deixou de apenas listar os eventos criados, agora sua função é de redirecionar o usuário para a página de um evento, sendo este evento o que ele clicou;

  A rota meus_eventos passou a realizar a antiga função de ver_eventos, listando todos os eventos criados por aquele usuário organizador;

  A rota editar_eventos leva o usuário Organizador para uma seção onde ele pode editar os dados de um evento previamente criado por ele;
```Python
@evento_bp.route('/Ver_eventos/<int:id>', methods=['GET'])
def visualizar_route(id):
    return visualizar(id)

@evento_bp.route('/meus_eventos',methods=['GET'])
@login_required
def meus_eventos_route():
    return meus_eventos()

@evento_bp.route('/editar_eventos/<int:id>', methods=['GET','POST'])
@login_required
def editar_route(id):
    return editar(id)
```

- Em inscrições:<br>
Agora com as rotas de inscrições, é possível se inscrever em eventos, visualizar os eventos em que está inscrito e para o usuário organizador 
visualizar quais usuários se inscreveram nos seus eventos;
```Python
@inscricoes_bp.route('/inscrever/<int:evento_id>', methods=['POST'])
@login_required
def inscrever(evento_id):
    return inscrever_evento(evento_id)

@inscricoes_bp.route('/minscricoes', methods=['GET'])
@login_required
def minhas_inscricoes():
    return visualizar_inscricoes_usuario()

@inscricoes_bp.route('/eventinscricoes/<int:id>',methods=['GET'])
@login_required
def inscritos_evento_route(id):
    return visualizar_inscritos_evento(id)
```

Na seção de controle:<br>

A função que verifica a extensão de arquivos de imagem, passou a ter um arquivo próprio, chamada de image_controller.py, facilitando sua utilização em outras partes do projeto:
```Python
from flask import current_app

#Função que verifica a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
```

Em auth_controller:<br>
Foi adicionado uma função de verificar por campos vazios tanto no registro quanto no login de usuários;
```Python
[...]
# Se os campos estiverem vazio
        if not nome.strip() or not email.strip() or not senha.strip():
            return render_template('register.html', mensagem='Os campos não podem estar vazios.')
[...]
```
  Também foi corrigido um bug no processo de login, que ocorria quando um e-mail inválido era informado. Isso causava uma falha na lógica da aplicação, ao tentar carregar a página de um usuário inexistente.
Para resolver esse problema, foi adicionado o seguinte trecho à função::
```Python
[...]
user = db.session.query(Usuario).filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.senha, senha):
            login_user(user)
        else:
            return render_template('login.html', mensagem='Email ou senha incorretos!')
[...]
```
Em usuario_controller:<br>
A função de edição dos dados do usuário foi refeita, corrigindo erros anteriores:
```Python
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
```

Inscricao_controller foi estabelecido:<br>
- A função inscrever_evento() é responsável por verificar se o usuário já está inscrito em determinado evento.
Ela recebe o ID do evento como parâmetro e consulta a tabela inscricoes para verificar se já existe uma inscrição com o mesmo ID de evento e o ID do usuário logado.
Caso não exista, uma nova inscrição é criada, vinculando o usuário ao evento.

- A função visualizar_inscricoes_usuario() permite que um usuário visualize todos os eventos nos quais está inscrito.
Para isso, ela realiza uma consulta que obtém os dados de cada evento associado ao usuário, com base nos registros da tabela inscricoes filtrados pelo ID do usuário logado.

- A função visualizar_inscritos_evento() permite que um organizador visualize todos os usuários inscritos em um evento criado por ele.
A consulta realizada busca o ID e o nome dos usuários inscritos, realizando um join com a tabela inscricoes e filtrando pelos eventos que correspondem ao ID consultado.
```Python
from datetime import date
from flask import redirect, render_template, url_for,flash
from flask_login import current_user
from app.services.database import db
from app.models import Eventos, Usuario, Inscricoes

def inscrever_evento(evento_id):
    usuario_id = current_user.id
    status = 'confirmado'

    # Verifica se já está inscrito, se quiser
    inscrito = Inscricoes.query.filter_by(usuario_id=usuario_id, eventos_id=evento_id).first()
    
    if inscrito:
        flash("Você já está inscrito neste evento.")
        return redirect(url_for('home.homepage'))

    nova_inscricao = Inscricoes(
        usuario_id=usuario_id,
        eventos_id=evento_id,
        data_inscricao = date.today(),
        status=status
        
    )
    db.session.add(nova_inscricao)
    db.session.commit()
    
    flash("Inscrição realizada com sucesso!")
    return redirect(url_for('home.homepage'))

def visualizar_inscricoes_usuario():
    usuario_id = current_user.id

    inscricoes = (
        db.session.query(Inscricoes, Eventos)
        .join(Eventos, Inscricoes.eventos_id == Eventos.id)
        .filter(Inscricoes.usuario_id == usuario_id)
        .all()
    )

    return render_template('minhas_inscricoes.html', inscricoes=inscricoes)

def visualizar_inscritos_evento(evento_id):
    id = evento_id

    inscritos = (
        db.session.query(Usuario.id, Usuario.nome)
        .select_from(Usuario)
        .join(Inscricoes, Usuario.id == Inscricoes.usuario_id)
        .filter(Inscricoes.eventos_id == id)
        .all()
    )

    return render_template('inscritos.html', inscritos = inscritos)
```

Em home_controller:<br>
Houve refatoração das lógicas de caminho para a página principal:
```Python
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
```

Em evento_controller:<br>
Agora a criação de eventos também envolve carregar a imagem de capa, adicionando uma genérica caso nenhuma for escolhida:
```Python
# salvando a imagem enviada
        imagem = request.files['fotoEventoForm']
        if imagem and imagem.filename != '' and allowed_file(imagem.filename):
            nome_seguro = secure_filename(imagem.filename)
            extensao = nome_seguro.rsplit('.', 1)[1]
            nome_unico = f"{uuid.uuid4().hex}.{extensao}"
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_unico)
            imagem.save(caminho)
            foto_evento_url = f"uploads/{nome_unico}"
        else:
            foto_evento_url = "default-event.png"
```

E como citado anteriormente na explicação das mudanças nas rotas, houve a adição de funções novas correspondentes a edição e visualização dos eventos:
```Python
# Função de visualização da página especifica de cada evento;
def visualizar(id):       
    if request.method == 'GET':
        evento = Eventos.query.get_or_404(id)
        criador = Usuario.query.get(evento.criador)
        return render_template("event_template.html",evento = evento, criador_nome = criador.nome)
    
def meus_eventos():
    if request.method == 'GET':
        eventos_usuario = Eventos.query.filter_by(criador=current_user.id).all()
        return render_template('visualizar.html', eventos=eventos_usuario)

def editar(id):
    evento = Eventos.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('editar.html',evento=evento)
    
    elif request.method == 'POST':
            evento.titulo = request.form['tituloForm']
            evento.data_inscricao = datetime.strptime(request.form['dataInscForm'], '%Y-%m-%d')
            evento.data_prazo = datetime.strptime(request.form['dataPrazoForm'], '%Y-%m-%d')
            evento.data_execucao = datetime.strptime(request.form['dataEventoForm'], '%Y-%m-%d')
            evento.localizacao = request.form['localizacaoForm']
            evento.descricao = request.form['descricaoForm']

            imagem = request.files['fotoEventoForm']
            if imagem and imagem.filename != '' and allowed_file(imagem.filename):
                nome_seguro = secure_filename(imagem.filename)
                extensao = nome_seguro.rsplit('.', 1)[1]
                nome_unico = f"{uuid.uuid4().hex}.{extensao}"
                caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_unico)
                imagem.save(caminho)
                evento.foto_evento_url = f"uploads/{nome_unico}"

            db.session.commit()
            flash("Evento atualizado com sucesso.", "success")
            return redirect(url_for('evento.meus_eventos_route'))
```


### 4. Autores
Pedro Alves
