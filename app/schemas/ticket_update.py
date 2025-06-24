from typing import Optional
from pydantic import BaseModel

class TicketUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    area: Optional[str] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    solicitante: Optional[str] = None
    comentario_interno: Optional[str] = None

