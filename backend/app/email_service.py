import resend

from .config import settings

resend.api_key = settings.resend_api_key


def enviar_codigo_verificacion(destinatario: str, nombre_usuario: str, codigo: str) -> None:
    resend.Emails.send(
        {
            "from": settings.email_remitente,
            "to": destinatario,
            "subject": "Tu código de verificación — SentimentBrand",
            "html": f"""
                <p>Hola {nombre_usuario},</p>
                <p>Tu código de verificación es:</p>
                <p style="font-size: 28px; font-weight: 700; letter-spacing: 4px;">{codigo}</p>
                <p>Vence en {settings.codigo_expira_minutos} minutos. Si no creaste esta
                cuenta, puedes ignorar este correo.</p>
            """,
        }
    )
