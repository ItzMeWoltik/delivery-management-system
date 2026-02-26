from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.orders import accept_order, decline_order, start_delivery, complete_delivery, transfer_order
from app.crud.orders import get_available_orders, get_active_orders, get_order_history
from app.services.geo import update_location
from app.services.pauses import check_pause_status
from app.core.i18n import translate

router = APIRouter()

@router.get("/orders/available")
def available_orders(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "courier":
        raise HTTPException(403)
    if check_pause_status(db, user.id):
        raise HTTPException(403, translate("on_pause"))
    orders = get_available_orders(db)
    return orders

@router.post("/orders/{order_id}/accept")
def accept(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    accept_order(db, order_id, user.id)
    return {"msg": translate("order_accepted")}

@router.post("/orders/{order_id}/decline")
def decline(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    decline_order(db, order_id, user.id)
    return {"msg": translate("order_declined")}

@router.post("/orders/{order_id}/start")
def start(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    start_delivery(db, order_id, user.id)
    return {"msg": translate("delivery_started")}

@router.post("/orders/{order_id}/complete")
def complete(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    complete_delivery(db, order_id, user.id)
    return {"msg": translate("delivery_completed")}

@router.post("/orders/{order_id}/transfer")
def transfer(order_id: int, to_courier_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    transfer_order(db, order_id, user.id, to_courier_id)
    return {"msg": translate("order_transferred")}

@router.get("/orders/active")
def active_orders(db: Session = Depends(get_db), user = Depends(get_current_user)):
    orders = get_active_orders(db, user.id)
    return orders

@router.get("/orders/history")
def history(db: Session = Depends(get_db), user = Depends(get_current_user)):
    orders = get_order_history(db, user.id)
    return orders

@router.post("/location/update")
def update_loc(lat: float, lon: float, db: Session = Depends(get_db), user = Depends(get_current_user)):
    update_location(db, user.id, lat, lon)
    return {"msg": translate("location_updated")}