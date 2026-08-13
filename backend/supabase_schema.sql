-- Ejecuta esto en Supabase → SQL Editor.
-- Si tu tabla "usuario" ya existe con otros nombres de columna,
-- comenta el CREATE TABLE y usa los ALTER TABLE ... RENAME COLUMN de abajo
-- reemplazando el nombre viejo por el nuevo.

create table if not exists usuario (
  correo             text primary key,
  password_hash      text not null,
  nombre_usuario     text not null,
  nombre_empresa     text not null,
  estado             text not null default 'pendiente', -- 'pendiente' | 'activo'
  codigo_verificacion text,          -- hash del código de 6 dígitos (nunca en texto plano)
  codigo_expira       timestamptz,   -- vencimiento del código (15 min desde su creación)
  creado_en           timestamptz not null default now()
);

-- Si tu tabla ya existía con otros nombres, ejemplos de renombrado:
-- alter table usuario rename column "contraseña" to password_hash;
-- alter table usuario rename column "usuario" to nombre_usuario;
-- alter table usuario rename column "empresa" to nombre_empresa;

-- Si la tabla ya existía pero le faltan las columnas del código de verificación:
-- alter table usuario add column if not exists codigo_verificacion text;
-- alter table usuario add column if not exists codigo_expira timestamptz;

-- Restringe los valores válidos de estado (opcional pero recomendado):
alter table usuario drop constraint if exists usuario_estado_check;
alter table usuario add constraint usuario_estado_check
  check (estado in ('pendiente', 'activo'));

-- IMPORTANTE: como el backend usa la service_role key (acceso administrativo,
-- solo del lado del servidor, nunca en el frontend), no necesitas políticas
-- de Row Level Security para que este backend funcione. Si más adelante
-- quieres que el frontend hable directo con Supabase (sin pasar por FastAPI),
-- ahí sí tendrías que habilitar y configurar RLS.
