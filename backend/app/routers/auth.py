from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..db import supabase, TABLA_USUARIO
from ..email_service import enviar_codigo_verificacion
from ..schemas import (
    LoginInput,
    MensajeOutput,
    ReenviarCodigoInput,
    RegistroInput,
    TokenOutput,
    VerificarInput,
)
from ..security import (
    calcular_expiracion_codigo,
    crear_token_sesion,
    generar_codigo_verificacion,
    hash_codigo,
    hash_password,
    verificar_codigo,
    verificar_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _buscar_usuario(correo: str) -> dict | None:
    resultado = supabase.table(TABLA_USUARIO).select("*").eq("correo", correo).execute()
    return resultado.data[0] if resultado.data else None


def _es_aware(dt: datetime) -> datetime:
    # Supabase devuelve timestamps con zona horaria como string; nos aseguramos
    # de compararlos correctamente contra "ahora" en UTC.
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


@router.post("/registro", response_model=MensajeOutput, status_code=201)
def registro(datos: RegistroInput):
    if _buscar_usuario(datos.correo):
        raise HTTPException(400, "Ese correo ya está registrado.")

    codigo = generar_codigo_verificacion()

    supabase.table(TABLA_USUARIO).insert(
        {
            "correo": datos.correo,
            "password_hash": hash_password(datos.password),
            "nombre_usuario": datos.nombre,
            "nombre_empresa": datos.empresa,
            "estado": "pendiente",
            "codigo_verificacion": hash_codigo(codigo),
            "codigo_expira": calcular_expiracion_codigo().isoformat(),
        }
    ).execute()

    enviar_codigo_verificacion(datos.correo, datos.nombre, codigo)

    return {"mensaje": "Cuenta creada. Revisa tu correo para verificarla."}


@router.post("/verificar", response_model=MensajeOutput)
def verificar(datos: VerificarInput):
    usuario = _buscar_usuario(datos.correo)
    if not usuario:
        raise HTTPException(404, "No existe una cuenta con ese correo.")

    if usuario["estado"] == "activo":
        return {"mensaje": "Esta cuenta ya estaba verificada."}

    if not usuario.get("codigo_verificacion") or not usuario.get("codigo_expira"):
        raise HTTPException(400, "No hay un código pendiente. Solicita uno nuevo.")

    expira = _es_aware(datetime.fromisoformat(usuario["codigo_expira"]))
    if expira < datetime.now(timezone.utc):
        raise HTTPException(400, "El código expiró. Solicita uno nuevo.")

    if not verificar_codigo(datos.codigo, usuario["codigo_verificacion"]):
        raise HTTPException(400, "Código incorrecto.")

    supabase.table(TABLA_USUARIO).update(
        {"estado": "activo", "codigo_verificacion": None, "codigo_expira": None}
    ).eq("correo", datos.correo).execute()

    return {"mensaje": "Cuenta verificada. Ya puedes iniciar sesión."}


@router.post("/reenviar-codigo", response_model=MensajeOutput)
def reenviar_codigo(datos: ReenviarCodigoInput):
    usuario = _buscar_usuario(datos.correo)
    if not usuario:
        raise HTTPException(404, "No existe una cuenta con ese correo.")

    if usuario["estado"] == "activo":
        raise HTTPException(400, "Esta cuenta ya está verificada.")

    codigo = generar_codigo_verificacion()
    supabase.table(TABLA_USUARIO).update(
        {
            "codigo_verificacion": hash_codigo(codigo),
            "codigo_expira": calcular_expiracion_codigo().isoformat(),
        }
    ).eq("correo", datos.correo).execute()

    enviar_codigo_verificacion(datos.correo, usuario["nombre_usuario"], codigo)

    return {"mensaje": "Nuevo código enviado. Revisa tu correo."}


@router.post("/login", response_model=TokenOutput)
def login(datos: LoginInput):
    usuario = _buscar_usuario(datos.correo)

    # Mensaje genérico ante correo inexistente o password incorrecta (no revelar cuál falló).
    credenciales_invalidas = HTTPException(401, "Correo o contraseña incorrectos.")

    if not usuario or not verificar_password(datos.password, usuario["password_hash"]):
        raise credenciales_invalidas

    if usuario["estado"] != "activo":
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Tu cuenta aún no ha sido verificada.",
                "codigo": "CUENTA_NO_VERIFICADA",
            },
        )

    token = crear_token_sesion(usuario["correo"])
    return {"access_token": token}
