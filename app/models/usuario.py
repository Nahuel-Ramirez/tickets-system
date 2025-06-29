from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum


class RolUsuario(str, enum.Enum):
    admin = "admin"
    operador = "operador"
    invitado = "invitado"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    contrasena = Column(String, nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False)
