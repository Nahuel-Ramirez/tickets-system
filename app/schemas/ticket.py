from pydantic import BaseModel
from datetime import datetime

class TicketOut(BaseModel):
    id: int
    titulo: str
    descripcion: str
    area: str
    fecha_creacion: datetime
    dias_atraso: int

    class Config:
        from_attributes = True


#Define que campos esperamos obtener cuando alguien crea un ticket
class TicketCreate(BaseModel):
    titulo: str
    descripcion: str
    area: str