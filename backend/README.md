# SentimentBrand — Backend (FastAPI + Supabase + Resend)

## 1. Preparar la base de datos

En Supabase → **SQL Editor**, corre `supabase_schema.sql` (está en esta carpeta).
Alinea los nombres de columna de tu tabla `usuario` con lo que espera el
código: `correo`, `password_hash`, `nombre_usuario`, `nombre_empresa`,
`estado`, `codigo_verificacion`, `codigo_expira`.

## 2. Instalar dependencias

```bash
cd backend
python -m venv venv
source venv/bin/activate   # en Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> Nota: esta sesión de trabajo no tiene salida a internet (ni a PyPI ni a
> npm), así que no pude ejecutar `pip install` aquí. Sí verifiqué la
> sintaxis de todos los archivos con `python -m py_compile`, pero corre la
> instalación real y las pruebas en tu máquina.

## 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Completa:
- `SUPABASE_URL` y `SUPABASE_SERVICE_KEY`: **Project Settings → API** en tu
  proyecto de Supabase. Usa la **service_role key** (no la `anon` key) — esta
  key tiene permisos administrativos y por eso nunca debe llegar al frontend,
  solo vive en el backend.
- `RESEND_API_KEY`: dashboard.resend.com → API Keys.
- `JWT_SECRET`: genera uno con `python -c "import secrets; print(secrets.token_hex(32))"`.

## 4. Correr el servidor

```bash
uvicorn app.main:app --reload
```

Abre `http://localhost:8000/docs` — ahí puedes probar cada endpoint
directamente sin necesidad del frontend.

## Endpoints implementados

| Método | Ruta | Qué hace |
|---|---|---|
| POST | `/auth/registro` | Crea el usuario (`estado = pendiente`), genera el código, lo guarda hasheado y envía el correo. |
| POST | `/auth/verificar` | Valida el código contra el hash guardado y su expiración; si es válido, pasa `estado` a `activo`. |
| POST | `/auth/reenviar-codigo` | Genera y envía un nuevo código si la cuenta sigue `pendiente`. |
| POST | `/auth/login` | Verifica correo/contraseña; si `estado != activo` responde `403` con `codigo: "CUENTA_NO_VERIFICADA"` (el frontend ya sabe leer esto); si todo es correcto, devuelve un JWT. |

## Cómo probarlo de punta a punta

1. Corre el backend (`uvicorn app.main:app --reload`) y el frontend (`pnpm dev:frontend`).
2. Regístrate desde `/registro` con un correo real al que tengas acceso.
3. Revisa tu bandeja de entrada (y spam) por el correo de Resend con el código.
4. Verifica el código en `/verificar`.
5. Inicia sesión en `/`.

## Notas de seguridad ya aplicadas

- Contraseñas y códigos de verificación se guardan **hasheados** (Argon2), nunca en texto plano.
- El código de verificación se genera con `secrets.randbelow` (criptográficamente seguro, no `random`).
- El login no revela si falló el correo o la contraseña (mensaje genérico), para no facilitar enumeración de cuentas.
- La `service_role key` de Supabase y el `RESEND_API_KEY` solo existen en el backend — nunca se exponen al navegador.

## Pendiente para una siguiente entrega

- Endpoint `GET /auth/me` (validar el JWT y devolver los datos del usuario logueado) para proteger `/inicio` en el frontend con datos reales.
- Rate limiting en `/auth/reenviar-codigo` y `/auth/login` para mitigar fuerza bruta.
- Manejo explícito de errores de Supabase/Resend (hoy se propagan como error 500 genérico).
