from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.chats import MessageCreate, TicketCreate
from app.crud.chats import create_message, get_chat_history, create_ticket, get_ticket_status

router = APIRouter()

@router.post("/messages")
def send_message(msg: MessageCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    create_message(db, msg, user.id)
    return {"msg": "Message sent"}

@router.get("/chats/{chat_id}/history")
def chat_history(chat_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    history = get_chat_history(db, chat_id, user.id)
    return history

@router.post("/tickets")
def create_support_ticket(ticket: TicketCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    ticket_id = create_ticket(db, ticket, user.id)
    return {"ticket_id": ticket_id}

@router.get("/tickets/{ticket_id}/status")
def ticket_status(ticket_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    status = get_ticket_status(db, ticket_id)
    return {"status": status}