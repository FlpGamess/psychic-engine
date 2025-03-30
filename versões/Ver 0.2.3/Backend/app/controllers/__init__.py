from .auth_controller import login, registrar, logout

from .evento_controller import criar, visualizar

from .home_controller import home

from .usuario_controller import upload_imagem, atualizar, deletar_usuario

__all__= [
    'login',
    'registrar',
    'logout',
    'criar',
    'vizualizar',
    'home',
    'upload_imagem',
    'atualizar',
    'deletar_usuario'
]
