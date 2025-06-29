from pydantic import BaseModel, EmailStr
from enum import Enum


class RolUsuario(str, Enum):
    admin = "admin"
    operador = "operador"
    invitado = "invitado"


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    contrasena: str
    rol: RolUsuario

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: RolUsuario

    class Config:
        from_attributes = True

