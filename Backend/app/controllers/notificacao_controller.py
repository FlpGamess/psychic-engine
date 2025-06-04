from app import db
from datetime import datetime
from app.models import Eventos, Usuario, Inscricoes, Notificacao
from flask_mail import Message
from app.services import mail

def notificacao_email():
    hoje = datetime.now().date()
    aviso_dias = 3  # Quantos dias antes avisar
    lista_usuarios = Usuario.query.all()

    for usuario in lista_usuarios:
        eventos_salvos = list(usuario.favoritos)
        inscricoes = (
            db.session.query(Inscricoes, Eventos)
            .join(Eventos, Inscricoes.eventos_id == Eventos.id)
            .filter(Inscricoes.usuario_id == usuario.id)
            .all()
        )

        eventos_inscritos = [evento for _, evento in inscricoes]

        eventos_a_notificar = []
        for evento in set(eventos_salvos + eventos_inscritos):
            if evento.data_execucao and 0 <= (evento.data_execucao.date() - hoje).days <= aviso_dias:
                eventos_a_notificar.append(evento)
        enviar_email(usuario, eventos_a_notificar)
                
def enviar_email(usuario, eventos):
    if not eventos:
        return

    corpo = "Olá, os seguintes eventos que você tem interesse estão se aproximando:\n\n"
    eventos_a_notificar = []

    for evento in eventos:
        ja_notificado = Notificacao.query.filter(Notificacao.usuario_id == usuario.id, Notificacao.eventos_id == evento.id).first()
        if not ja_notificado:
            eventos_a_notificar.append(evento)
            corpo += f"- {evento.titulo} em {evento.data_execucao.strftime('%d/%m/%Y')}\n"

    if eventos_a_notificar:
        msg = Message(
            subject="Lembrete de eventos próximos",
            recipients=[usuario.email],
            body=corpo
        )

        # Criando uma string representando o conteúdo do email
        mensagem_str = f"""\
        Assunto: {msg.subject}
        Para: {', '.join(msg.recipients)}

        {msg.body}
        """
        for evento in eventos_a_notificar:
            nova_notificacao = Notificacao(
                usuario_id = usuario.id,
                eventos_id = evento.id,
                mensagem = mensagem_str,
                data_envio = datetime.now().date()
            )
            db.session.add(nova_notificacao)
        db.session.commit()
        mail.send(msg)


def enviar_email_convite(usuario_email, link_evento):
    msg = Message(
        subject="Convite para Evento Online",
        recipients=[usuario_email],
        body=f"Olá! Você está convidado para participar do evento online. Acesse pelo link: {link_evento}"
    )
    mail.send(msg)