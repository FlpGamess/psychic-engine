from datetime import datetime
from app.controllers.notificacao_controller import notificacao_email
from app import create_app
from flask_apscheduler import APScheduler

app = create_app()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Tarefa agendada: executa imediatamente e depois a cada 1 dia
scheduler.add_job(
    id='enviar_emails_diariamente',
    func=lambda: executar_notificacao_com_contexto(),
    trigger='interval',
    days=1,
    next_run_time=datetime.now()  # Executa imediatamente ao iniciar o servidor
)

def executar_notificacao_com_contexto():
    with app.app_context():
        notificacao_email()

if __name__== "__main__":
    app.run(debug=True)