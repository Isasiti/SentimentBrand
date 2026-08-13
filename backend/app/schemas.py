from pydantic import BaseModel, EmailStr, Field


class RegistroInput(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    empresa: str = Field(min_length=1, max_length=120)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)

class VerificarInput(BaseModel):
    correo: EmailStr
    codigo: str = Field(min_length=6, max_length=6)


class ReenviarCodigoInput(BaseModel):
    correo: EmailStr


class LoginInput(BaseModel):
    correo: EmailStr
    password: str


class MensajeOutput(BaseModel):
    mensaje: str


class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"
