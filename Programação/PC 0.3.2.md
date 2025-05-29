
## Procedimento de Compilação

<!-- Aqui fica o cabeçalho, onde teremos informações rápidas sobre as modificações do procedimento-->
<div align="center">
    <table border="1">
        <thead>
            <tr>
                <th><strong>CÓDIGO</stron></th>
                <th><strong>TÍTULO</strong></th>
                <th><strong>STATUS</strong></th>
                <th><strong>DATA DA REVISÃO</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>PC-0.3.2</td>
                <td>Limite de Vagas e Exclusão de Eventos</td>
                <td>Compilado</td>
                <td>28/05/2025</td>
            </tr>
        </tbody>
    </table>
</div>

## 1. Geral
- Implementação do campo limite na tabela Eventos, permitindo que usuários estabeleçam opcionalmente um número de vagas limitadas para os eventos.
- Foi adicionado a opção de deletar eventos.


## 2. Mudanças
Adição do campo limite na tabela Model de Eventos:
```Python
from app import db
from app.models.evento_tags import evento_tags

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
    foto_evento_url = db.Column(db.String(255))
    limite = db.Column(db.Integer, nullable=True)

    tags = db.relationship(
    'Tags',
    secondary=evento_tags,
    backref='eventos',
    lazy='subquery'
    )

    def __init__(self, titulo, data_inscricao,data_prazo,data_execucao,localizacao,descricao,criador,foto_evento_url,limite):
        self.titulo = titulo
        self.data_inscricao = data_inscricao
        self.data_execucao = data_execucao
        self.data_prazo = data_prazo
        self.localizacao = localizacao
        self.descricao = descricao
        self.criador = criador
        self.foto_evento_url = foto_evento_url
        self.limite = limite
    
```
Em evento_controller foi adicionado o tratamento de campo vazio no limite, dessa forma definindo o limite para 0 o que significa que não há limite de vagas.
```Python
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
        limite = request.form['limiteForm']

        if limite == '':
            limite = 0

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

        novo_evento = Eventos(
            titulo=titulo,
            data_inscricao=data_inscricao,
            data_prazo=data_prazo,
            data_execucao=data_execucao,
            localizacao=localizacao,
            descricao=descricao, 
            criador=criador,
            foto_evento_url=foto_evento_url,
            limite=limite)
        
        #======== Lógica das tags ===========================================================================================================================================================
        tags_texto = request.form['tagsForm']
        nomes_tags = re.findall(r'#(\w+)', tags_texto)  # Extrai: ['tech', 'web', 'cultura']

        for nome_tag in nomes_tags:
            tag = Tags.query.filter_by(nome=nome_tag).first()
            if not tag:
                tag = Tags(nome=nome_tag)
                db.session.add(tag)
            novo_evento.tags.append(tag)
        
        db.session.add(novo_evento)
        db.session.commit()
    
        return redirect(url_for('home.homepage'))  # Redireciona para a página inicial após criar o evento
```

O mesmo foi feito para a função editar:
```Python
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
            limite = request.form['limiteForm']

            if limite == '':
                limite = 0
            evento.limite = limite

            imagem = request.files['fotoEventoForm']
            if imagem and imagem.filename != '' and allowed_file(imagem.filename):
                nome_seguro = secure_filename(imagem.filename)
                extensao = nome_seguro.rsplit('.', 1)[1]
                nome_unico = f"{uuid.uuid4().hex}.{extensao}"
                caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_unico)
                imagem.save(caminho)
                evento.foto_evento_url = f"uploads/{nome_unico}"

            #======== Lógica das tags ===========================================================================================================================================================
            tags_texto = request.form['tagsForm']
            nomes_tags = re.findall(r'#(\w+)', tags_texto) 

            for nome_tag in nomes_tags:
                tag = Tags.query.filter_by(nome=nome_tag).first()
                if not tag:
                    tag = Tags(nome=nome_tag)
                    db.session.add(tag)
                evento.tags.append(tag)

            db.session.commit()

            flash("Evento atualizado com sucesso.", "success")
            return redirect(url_for('evento.meus_eventos_route'))
```
Função de excluir:<br>
Ela primeiro consulta o evento pelo id recebido e então exclui a imagem carregada deste evento, depois exclui todas as inscrições feitas naquele evento e por último o próprio evento.
```Python
def excluir(id):
    evento = Eventos.query.get_or_404(id)
    inscricoes = Inscricoes.query.filter_by(eventos_id = evento.id).all()
    # Exclui a foto do evento se existir
    if evento.foto_evento_url:
        caminho_imagem = os.path.join(current_app.config['UPLOAD_FOLDER'], evento.foto_evento_url.split('/')[-1])
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)

    # Exclui as Inscricoes relacionadas ao Evento excluido
    for inscricao in inscricoes:
        db.session.delete(inscricao)
    # Exclui o Evento do banco de dados
    db.session.delete(evento)

    db.session.commit()

    return redirect(url_for('evento.meus_eventos_route'))
```

adaptações na exibição do html foram feitas para comportar essas mudanças

### 4. Autores
Pedro Alves
