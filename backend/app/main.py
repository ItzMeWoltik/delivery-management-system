from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.api.endpoints import auth, customers, couriers, admin, payments, chats, geo
from app.db.session import engine
from app.db.base import Base
from app.core.config import settings
from app.core.i18n import translate
from app.services.chats import ChatManager

app = FastAPI(title="Delivery Management System")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(couriers.router, prefix="/couriers", tags=["couriers"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])
app.include_router(geo.router, prefix="/geo", tags=["geo"])

chat_manager = ChatManager()

@app.get("/")
def root():
    return {"message": translate("welcome")}

@app.get("/lang-select")
def lang_select(lang: str = "EN"):
    if lang not in ["EN", "UA"]:
        lang = "EN"
    return {"lang": lang, "message": translate("selected_lang", lang=lang)}

@app.websocket("/ws/chat/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await chat_manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.send(data, room)
    except WebSocketDisconnect:
        chat_manager.disconnect(room)