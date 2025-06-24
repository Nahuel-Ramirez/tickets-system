#Creando las rutas base

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ticket import Ticket
from app.schemas.ticket import TicketOut
from typing import List


router = APIRouter()

# #Simulamos base de datos
# fake_db = [
#     Ticket(id=1, titulo="Actualizar excel", area="Pagos", pedido="Actualizar formulas en archivo mensual", estado="Pendiente"),
#     Ticket(id=2, titulo="Acceso VPN", area="Cobranza", pedido="Configurar notebook en nueva Notebook", estado="En curso")
# ]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Creamos la ruta /tickets para listar (metodo GET) y crear (metodo POST) tickets con una base de datos falsa.
@router.get("/tickets", response_model=List[TicketOut])
def listar_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()


