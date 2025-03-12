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
foi adicionada uma nova rota a /deletar que realiza requisições GET e POST, ao chamar a função deletar_usuario onde caso o usuario tenha uma foto ela ira ser excluida da pasta uploads, após isto excluira o usuario do banco com todas suas informações e sera realizado o logout fazendo com que o usuario volte para a homepage, porem com a conta inteiramente deletada

```Python
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
    
```

**homepage.html**
Foi adicionado um botão de deletar conta onde caso o usuario aperte ira perguntar se ele tem certeza e caso confirme sera chamada a rota deletar_usuario.
linhas adicionadas:109,110,162 a 165


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
        .logout-button, .login-button, .register-button, .atulization-button, .delete-button {
            margin-top: 20px;
            padding: 10px 20px;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .logout-button, .atulization-button {
            background-color: #ff4d4d;
        }
        .logout-button:hover, .atulization-button:hover {
            background-color: #cc0000;
        }
        .delete-button {
            background-color: #ff0000; /* Vermelho */
        }
        .delete-button:hover {
            background-color: #cc0000; /* Vermelho mais escuro */
        }
        .login-button, .register-button {
            background-color: #cc0000; /* Vermelho */
        }
        .login-button:hover, .register-button:hover {
            background-color: #cc0000; /* Vermelho */
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

        <!-- Botão de Deletar Conta -->
        <form action="{{ url_for('deletar_usuario') }}" method="post" onsubmit="return confirm('Tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita.');">
            <button type="submit" class="delete-button">Deletar Conta</button>
        </form>
    </div>
    {% else %}
    <div class="container">
        <h1>Você não está logado, irmão.</h1>
        <!-- Botão de Login -->
        <a href="{{ url_for('login') }}">
            <button type="button" class="login-button">Login</button>
        </a>
        <!-- Botão de Registrar -->
        <a href="{{ url_for('registrar') }}">
            <button type="button" class="register-button">Registrar</button>
        </a>
    </div>
    {% endif %}
</body>
</html>
```

### 3. Autores
Felipe Pereira da Silva

Vulgo FlpGamess.
