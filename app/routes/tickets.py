#Creando las rutas base

from fastapi import APIRouter
from app.models.ticket import Ticket

router = APIRouter()

#Simulamos base de datos
fake_db = [
    Ticket(id=1, titulo="Actualizar excel", area="Pagos", pedido="Actualizar formulas en archivo mensual", estado="Pendiente"),
    Ticket(id=2, titulo="Acceso VPN", area="Cobranza", pedido="Configurar notebook en nueva Notebook", estado="En curso")
]

#Creamos la ruta /tickets para listar (metodo GET) y crear (metodo POST) tickets con una base de datos falsa.
@router.get("/tickets")
def listar_tickets():
    return fake_db

@router.post("/tickets")
def crear_tickets(ticket:Ticket):
    fake_db.append(ticket)
    return ticket

