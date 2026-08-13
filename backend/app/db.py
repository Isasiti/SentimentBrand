from supabase import create_client, Client
from .config import settings

# Cliente único, reutilizado en toda la app. Usa la service_role key:
# tiene acceso administrativo a la tabla y omite Row Level Security,
# por eso esta key vive SOLO en el backend (nunca en el frontend).
supabase: Client = create_client(settings.supabase_url, settings.supabase_service_key)

TABLA_USUARIO = "usuario"
