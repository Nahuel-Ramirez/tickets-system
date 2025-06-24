# Creamos el modelo del ticket. Simulado, sin base de datos.

# from pydantic import BaseModel
# from typing import Literal

# class Ticket(BaseModel):
#     id: int
#     titulo: str
#     area: Literal["Contabilidad", "Pagos", "Cobranza", "Tesoreria", "Gerencia", "Otros"]
#     pedido: str
#     estado: Literal["Pendiente", "En curso", "Completado"]


from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    area = Column(String, nullable=False)
    estado = Column(String, default="Pendiente")
    solicitante = Column(String, nullable=False, default="Desconocido")
    fecha_creacion = Column(DateTime, default=datetime.now)
    prioridad = Column(String, nullable=False, default="Baja")
    comentario_interno = Column(Text, nullable=True)

