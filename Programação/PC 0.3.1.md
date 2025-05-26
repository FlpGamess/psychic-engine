
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
                <td>PC-0.3.1</td>
                <td>Implementação de Tags</td>
                <td>Compilado</td>
                <td>26/05/2025</td>
            </tr>
        </tbody>
    </table>
</div>

## 1. Geral
- Foi implementado a lógica de criação e atribuição de Tags à eventos, para tal
foi necessário criar uma nova tabela de entidade e uma tabela intermediária evento_tags que faz a ponte para o relacionamento N:N entre Tags e Eventos;
- Agora Usuários podem pesquisar por Tags ao buscar eventos na página principal;


## 2. Mudanças
Model de tags.py e evento_tags.py :<br>
```Python
from app import db

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)

    def __init__(self,nome):
        self.nome = nome
```
A tabela evento_tags não contém método construtor, pois é apenas uma tabela intermediária de relação.
```Python
from app import db

evento_tags  = db.Table('evento_tags',
    db.Column('eventos_id', db.Integer, db.ForeignKey('eventos.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)
```

Foi adicionado o seguinte campo à tabela Eventos:
```Python
tags = db.relationship(
    'Tags',
    secondary=evento_tags,
    backref='eventos',
    lazy='subquery'
    )
```
Ele define a variavel tags como um campo de Eventos que recebe uma lista de Tags, intermediada pela tabela evento_tags, definida no parâmetro **secondary**, o parâmetro **backref** permite consultas contrarias;
e o campo **lazy** define o método de consulta, no caso foi utilizado como **subquery** para que a consulta fosse otimizada, trazendo todas as Tags pertencentes de uma única vez.<br>

Mudança Feita nos controllers:<br>
Em eventos_controllers houve uma adaptação dos métodos de criar e editar eventos, com a adição da lógica de atribuir tags aos eventos durante esses 2 processos. A lógica segue um modelo simples de verificação se essa Tag
já existe, caso exista ela é atribuida ao Evento, caso não seja uma tag nova é criada na tabela Tags e sua atribuição é feita; Permitindo assim a criação de diversas Tags não convencionais para os usuários 
marcarem seus eventos.
```Python
tags_texto = request.form['tagsForm']
nomes_tags = re.findall(r'#(\w+)', tags_texto)  # Extrai: ['tech', 'web', 'cultura']

for nome_tag in nomes_tags:
    tag = Tags.query.filter_by(nome=nome_tag).first()
    if not tag:
        tag = Tags(nome=nome_tag)
        db.session.add(tag)
    novo_evento.tags.append(tag)
```

A lógica de pesquisa de Eventos ficou da seguinte forma:
```Python
def home():
    termo = request.args.get('q', '').strip()

    if termo:
        lista_eventos = (
            Eventos.query
            .outerjoin(Eventos.tags)  # relacionamento definido com secondary
            .options(joinedload(Eventos.tags))  # evita N+1 queries
            .filter(
                or_(
                    Eventos.titulo.ilike(f"%{termo}%"),
                    Tags.nome.ilike(f"%{termo}%")
                )
            )
            .distinct()
            .all()
        )
    else:
        lista_eventos = Eventos.query.all()
    
    return render_template("homepage.html", lista_eventos = lista_eventos,termo=termo)
```

Assim, a consulta de busca por eventos realiza um outer join com a tabela de tags, permitindo filtrar não apenas pelo título do evento, mas também pelos nomes das tags associadas que contenham o termo pesquisado.<br>

Mudanças feitas nas páginas de exibição:<br>
Em criar.html:
```Html
<div class="col-md-12">
  <label for="tags">Tags (use `#` para separá-las):</label>
  <input type="text" name="tagsForm" placeholder="#tags">
</div>
```
e em editar.html:
```Html
<div class="mb-3">
  <label for="tags" class="form-label">Tags (use `#` para separá-las):</label>
  <input type="text" name="tagsForm" placeholder="#tags">
</div>
```

E em homepage.html e user_homepage.html foi adicionado o seguinte trecho de exibição das tags logo abaixo do título:
```html
{% if item.tags %}
<div class="mt-4">
    <h5 class="fw-bold">Tags:</h5>
    <div class="d-flex flex-wrap justify-content-center gap-2 mt-2">
        {% for tag in item.tags %}
            <span class="badge bg-primary fs-6">#{{ tag.nome }}</span>
        {% endfor %}
    </div>
</div>
{% endif %}
```

### 4. Autores
Pedro Alves
