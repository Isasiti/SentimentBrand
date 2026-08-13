# SentimentBrand — Monorepo

```
sentimentbrand/
├── Frontend/   → Vue 3 + Vite (esta entrega)
└── backend/    → FastAPI (próxima entrega)
```

## Gestor de paquetes: pnpm

Si no tienes pnpm instalado:

```bash
corepack enable
corepack prepare pnpm@9.12.0 --activate
```

`corepack` viene incluido con Node.js 16.9+; así usas exactamente la versión
de pnpm declarada en `packageManager` de cada `package.json`.

El `.npmrc` en la raíz incluye `minimum-release-age=1440`: pnpm no instalará
una versión de un paquete hasta que lleve 24 horas publicada en el registro,
como margen de seguridad ante paquetes comprometidos recién publicados.

## Cómo correrlo

```bash
cd sentimentbrand      # raíz del monorepo
pnpm install           # instala Frontend/ vía el workspace
cp Frontend/.env.example Frontend/.env
pnpm dev:frontend
# alternativa equivalente: cd Frontend && pnpm dev
```

Abre `http://localhost:5173`.

> Nota: el paquete no incluye `node_modules` ni `pnpm-lock.yaml` — esta
> sesión de trabajo no tiene salida a internet para instalar dependencias.
> Corre `pnpm install` en tu propia máquina; ahí se genera el lockfile, que
> sí debes versionar en git (a diferencia de `node_modules`).

## Flujo de autenticación implementado en esta entrega

Ya no se usa Google Auth. El flujo ahora es:

1. **`/registro`** — el usuario ingresa nombre, empresa, correo y contraseña
   (con confirmación y validación de mínimo 8 caracteres). Envía
   `POST {VITE_API_URL}/auth/registro`.
2. Al registrarse exitosamente, se redirige a **`/verificar?correo=...`**,
   donde el usuario ingresa el código de 6 dígitos que le llegó por correo.
   Envía `POST {VITE_API_URL}/auth/verificar`. Incluye botón de
   "reenviar código" (`POST {VITE_API_URL}/auth/reenviar-codigo`).
3. **`/`** (login) — correo + contraseña. Envía
   `POST {VITE_API_URL}/auth/login`. Si el backend responde que la cuenta no
   está verificada, muestra un enlace directo a `/verificar`.
4. Al iniciar sesión, guarda `access_token` en `localStorage` y redirige a
   `/inicio` (placeholder protegido por guarda de navegación).

**Ninguno de estos endpoints existe todavía en el backend** — por eso, al
probar el frontend ahora, verás "no se pudo conectar con el servidor" al
enviar cualquier formulario. Es el comportamiento esperado hasta que
construyamos el backend en FastAPI (registro, envío del código por correo
con Resend, verificación y login).

### Componentes reutilizables

`src/components/BrandPanel.vue` contiene el panel de marca (el "pulso de
sentimiento" animado) que comparten las tres pantallas de autenticación, con
un `caption` distinto en cada una.
