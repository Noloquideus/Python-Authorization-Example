from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from src.config import settings
from src.infrastructure.tasks.celery_app import celery

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True)


@celery.task(name="send_confirmation_email")
def send_confirmation_email(to: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=body,
        subtype=MessageType.html)
    fm = FastMail(conf)
    fm.send_message(message)
