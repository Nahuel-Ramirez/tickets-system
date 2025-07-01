#Creando las rutas base

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ticket import Ticket
from app.schemas.ticket import TicketOut, TicketCreate
from datetime import datetime
from app.schemas import ticket as schemas
from app.schemas import ticket_update as schema_ticketupdate
from fastapi.responses import JSONResponse
from app.utils.ticket_utils import to_ticket_out
from app.auth.dependencies import is_admin, is_operador
from app.models.usuario import Usuario
from typing import List


router = APIRouter()

#Obtenemos la sesion de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#Creamos la ruta /tickets para listar (metodo GET).
@router.get("/tickets", response_model=List[TicketOut])
def listar_tickets(
    estado: str = Query(None),
    area: str = Query(None),
    prioridad: str = Query(None),
    db: Session = Depends(get_db)):

    query = db.query(Ticket)

    if estado:
        query = query.filter(Ticket.estado == estado)
    if area:
        query = query.filter(Ticket.area == area)
    if prioridad:
        query = query.filter(Ticket.prioridad == prioridad)

    tickets = query.all()
    return [to_ticket_out(t) for t in tickets]

#Creamos la ruta para listar por un ID especifico.
@router.get("/tickets/{ticket_id}", response_model=schemas.TicketOut)
def get_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket


#Creamos la ruta /tickets para crear un nuevo ticket (metodo POST)
@router.post("/tickets", response_model=TicketOut)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db), user: Usuario = Depends(is_operador)):
    nuevo_ticket = Ticket(
        titulo=ticket.titulo,
        descripcion=ticket.descripcion,
        area=ticket.area
    )
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    return to_ticket_out(nuevo_ticket)


#Creamos la ruta /ticket/{id} para actualizar parcialmente el ticket.
@router.patch("/tickets/{ticket_id}", response_model=schemas.TicketOut)
def update_ticket(ticket_id: int, ticket_update: schema_ticketupdate.TicketUpdate, db: Session = Depends(get_db), user: Usuario = Depends(is_operador)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    for field, value in ticket_update.model_dump(exclude_unset=True).items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    return to_ticket_out(ticket)

#Creamos la ruta /tickets/{ticket_id} para eliminar tickets con metodo DELETE
@router.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), user: Usuario = Depends(is_admin)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    db.delete(ticket)
    db.commit()
    return JSONResponse(content={"mensaje": f"Ticket con ID {ticket_id} eliminado correctamente"}, status_code=200)
