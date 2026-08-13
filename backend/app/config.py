from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Supabase (Project Settings → API en el dashboard de Supabase)
    supabase_url: str
    supabase_service_key: str  # service_role key: SOLO en el backend, nunca en el frontend

    # Resend (dashboard.resend.com → API Keys)
    resend_api_key: str
    email_remitente: str = "SentimentBrand <onboarding@resend.dev>"

    # JWT propio de la app (para las sesiones, luego de que Supabase ya no interviene)
    jwt_secret: str
    jwt_expira_minutos: int = 60 * 24  # 24 horas

    # Código de verificación
    codigo_expira_minutos: int = 15

    # CORS: origen del frontend en desarrollo
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
