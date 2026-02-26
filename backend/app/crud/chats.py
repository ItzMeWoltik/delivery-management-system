from sqlalchemy.orm import Session
from app.db.models.chats import Message, Ticket
from .base import CRUDBase

class CRUDMessage(CRUDBase[Message]):
    def get_history(self, db: Session, chat_id: int, user_id: int):
        return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp).all()

class CRUDTicket(CRUDBase[Ticket]):
    def get_status(self, db: Session, ticket_id: int):
        ticket = self.get(db, ticket_id)
        return ticket.status if ticket else None

message = CRUDMessage(Message)
ticket = CRUDTicket(Ticket)
create_message = message.create
get_chat_history = message.get_history
create_ticket = ticket.create
get_ticket_status = ticket.get_status