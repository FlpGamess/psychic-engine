from .auth_controller import login, registrar, logout

from .evento_controller import criar, visualizar, meus_eventos, editar

from .home_controller import home, user_home

from .image_controller import allowed_file

from .inscricoes_controller import inscrever_evento, visualizar_inscricoes_usuario, visualizar_inscritos_evento

from .usuario_controller import upload_imagem_perfil, atualizar, deletar_usuario, modo_organizador, perfil

__all__= [
    'login',
    'registrar',
    'logout',
    'criar',
    'visualizar',
    'meus_eventos',
    'editar',
    'home',
    'user_home',
    'allowed_file',
    'inscrever_evento', 
    'visualizar_inscricoes_usuario', 
    'visualizar_inscritos_evento',
    'upload_imagem_perfil',
    'atualizar',
    'deletar_usuario',
    'modo_organizador',
    'perfil'
]
