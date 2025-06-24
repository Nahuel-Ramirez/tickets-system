#Creando las rutas base

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ticket import Ticket
from app.schemas.ticket import TicketOut, TicketCreate
from datetime import datetime
from app.schemas import ticket as schemas
from app.schemas import ticket_update as schema_ticketupdate
from typing import List


router = APIRouter()

# #Simulamos base de datos
# fake_db = [
#     Ticket(id=1, titulo="Actualizar excel", area="Pagos", pedido="Actualizar formulas en archivo mensual", estado="Pendiente"),
#     Ticket(id=2, titulo="Acceso VPN", area="Cobranza", pedido="Configurar notebook en nueva Notebook", estado="En curso")
# ]

#Obtenemos la sesion de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def to_ticket_out(ticket: Ticket) -> TicketOut:
       return TicketOut(
    id=ticket.id,
    titulo=ticket.titulo,
    descripcion=ticket.descripcion,
    area=ticket.area,
    estado=ticket.estado,
    solicitante=ticket.solicitante,
    fecha_creacion=ticket.fecha_creacion,
    prioridad=ticket.prioridad,
    comentario_interno=ticket.comentario_interno,
    dias_atraso=(datetime.now() - ticket.fecha_creacion).days
)

#Creamos la ruta /tickets para listar (metodo GET).
@router.get("/tickets", response_model=List[TicketOut])
def listar_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    resultado = []

    for t in tickets:
        resultado.append(TicketOut(
            id=t.id,
            titulo=t.titulo,
            descripcion=t.descripcion,
            area=t.area,
            estado=t.estado,
            solicitante=t.solicitante,
            fecha_creacion=t.fecha_creacion,
            prioridad=t.prioridad,
            comentario_interno=t.comentario_interno,
            dias_atraso=(datetime.now()-t.fecha_creacion).days
        ))
    return resultado

#Creamos la ruta para listar por un ID especifico.
@router.get("/tickets/{ticket_id}", response_model=schemas.TicketOut)
def get_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

#Creamos la ruta /tickets para crear un nuevo ticket (metodo POST)
@router.post("/tickets", response_model=TicketOut)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    nuevo_ticket = Ticket(
        titulo=ticket.titulo,
        descripcion=ticket.descripcion,
        area=ticket.area
    )
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    return nuevo_ticket


#Creamos la ruta /ticket/{id} para actualizar parcialmente el ticket.
@router.patch("/tickets/{ticket_id}", response_model=schemas.TicketOut)
def update_ticket(ticket_id: int, ticket_update: schema_ticketupdate.TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    for field, value in ticket_update.model_dump(exclude_unset=True).items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    return to_ticket_out(ticket)