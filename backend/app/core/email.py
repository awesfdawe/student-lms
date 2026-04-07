from email.message import EmailMessage
import aiosmtplib
from app.core.config import settings


async def send_email(to, subject, body):
    message = EmailMessage()
    message["From"] = settings.SMTP_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    kwargs = {
        "hostname": settings.SMTP_HOST,
        "port": settings.SMTP_PORT,
    }

    if settings.SMTP_USER:
        kwargs["username"] = settings.SMTP_USER
        kwargs["password"] = settings.SMTP_PASSWORD

    await aiosmtplib.send(message, **kwargs)
