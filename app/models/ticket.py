# Creamos el modelo del ticket. Simulado, sin base de datos.

from pydantic import BaseModel
from typing import Literal

class Ticket(BaseModel):
    id: int
    titulo: str
    area: Literal["Contabilidad", "Pagos", "Cobranza", "Tesoreria", "Gerencia", "Otros"]
    pedido: str
    estado: Literal["Pendiente", "En curso", "Completado"]