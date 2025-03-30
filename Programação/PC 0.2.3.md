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
                <td>PC-0.2-03</td>
                <td>Organização de pastas</td>
                <td>Compilado</td>
                <td>30/03/2025</td>
            </tr>
        </tbody>
    </table>
</div>

### 1. Geral
O Projeto foi reorganizado, separando suas devidas funções em pastas especificas, com o objetivo de facilitar a compreensão.


## 2. Mudanças

Nova estrutura das pastas:
```
  app/
  ├── controller/
  ├── models/
  ├── routes/
  ├── services/
  ├── static/
  ├── templates/
  ├── __init__.py
  main.py
```

Responsabilidade das novas pastas:

  controller/: Contém a lógica principal do sistema.
  
  models/: Contém as definições do banco de dados com SQLAlchemy.
  
  routes/: Define as rotas da aplicação.
  
  services/: Contém funções auxiliares e regras de negócio.

  1 -  main.py agora apenas importa a função create_app de app/__init__.py e executa a aplicação:

  ```Python
  from app import create_app
  
  app = create_app()
  app.run(debug=True)
  ```

  2 - Na subpasta models, agora cada arquivo é referente a entidade que representa, seguindo a seguinte estrutura:
  ```
  models/
  ├── usuario.py
  ├── eventos.py
   ```
  3 - Na subpasta controllers agora armazena a lógica principal do sistema, tendo como adição notavel a pasta /auth_controller que armazena a lógica de login e registro de um usuário; e a pasta usuario_controller que foi feita para armazenar a lógica
de atualização de dados do usuário , caso de pedido de descadastro (deletar usuário) ou troca de modos (do modo Participante para modo Organizador);

  4 - Na subpasta routes se encontram as Blueprints, que organizam as rotas da aplicação. Elas têm a função de definir e registrar as rotas, associando cada uma a uma função específica, facilitando o roteamento e a modularização da aplicação.

  5 - A pasta services contém a configuração e exportação das instâncias de Bcrypt e SQLAlchemy, responsáveis respectivamente pela criptografia de senhas e pela comunicação com o banco de dados. 

## 3. Códigos adicionados:
  Foi feito uma função de validação de email para o cadastro de usuários novos, não permitindo o cadastro no caso do email ja ser utilziado por outro usuário;
  Esta função está presente no arquivo usuario_controller:
  ```Python
def verificar_email(email):                     # Função para verifica se o email já foi cadastrado;
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario != None:
        return True
  ```

  Também foi feito uma versão inicial da separação dos modos de usuário, no qual para esta primeira versão o "Modo organizador é um jeito de separar uma tela exclusiva para criação de eventos.
  ```Python
  def modo_organizador():
    return render_template('creationhub.html')
  ```
  Rota referente ao modo organizador, localizada em routes:
  ```Python
  @usuario_bp.route('/organizador', methods=['GET'])
  @login_required
  def organizador_route():
      return modo_organizador()
   ```


### 4. Autores
Pedro Alves
