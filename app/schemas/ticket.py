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
        orm_mode = True
