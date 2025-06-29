from app.models import Ticket
from app.schemas.ticket import TicketOut
from datetime import datetime

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