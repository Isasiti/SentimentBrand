import secrets
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verificar_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def generar_codigo_verificacion() -> str:
    """6 dígitos, generados con un generador criptográficamente seguro (no random.randint)."""
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_codigo(codigo: str) -> str:
    # El código se guarda hasheado igual que la contraseña: nunca en texto plano en la BD.
    return pwd_context.hash(codigo)


def verificar_codigo(codigo: str, codigo_hash: str) -> bool:
    return pwd_context.verify(codigo, codigo_hash)


def calcular_expiracion_codigo() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=settings.codigo_expira_minutos)


def crear_token_sesion(correo: str) -> str:
    payload = {
        "sub": correo,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expira_minutos),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decodificar_token_sesion(token: str) -> str:
    """Devuelve el correo (sub) si el token es válido; lanza jwt.PyJWTError si no."""
    payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    return payload["sub"]
