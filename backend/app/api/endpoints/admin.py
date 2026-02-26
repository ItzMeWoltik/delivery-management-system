from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, get_current_user
from app.db.models.orders import Order
from app.db.models.payments import Payment
from app.db.models.users import User
from app.crud.orders import get_all_orders, force_cancel_order, force_complete_order, manual_transfer_order
from app.services.fraud import get_fraud_alerts
from app.services.pauses import apply_pause
from app.core.i18n import translate

router = APIRouter()

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    live_deliveries = db.query(Order).filter(Order.status == "in_transit").count()
    revenue = db.query(func.sum(Payment.amount)).filter(Payment.status == "paid").scalar() or 0
    active_couriers = db.query(User).filter(User.role == "courier", User.is_active == True).count()
    return {"live_deliveries": live_deliveries, "revenue": revenue, "active_couriers": active_couriers}

@router.get("/alerts")
def alerts(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    fraud_alerts = get_fraud_alerts(db)
    return fraud_alerts

@router.post("/pauses/apply/{courier_id}")
def apply(courier_id: int, duration: int, reason: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    apply_pause(db, courier_id, duration, reason)
    return {"msg": translate("pause_applied")}

@router.get("/orders")
def all_orders(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    orders = get_all_orders(db)
    return orders

@router.post("/orders/{order_id}/force_cancel")
def force_cancel(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    force_cancel_order(db, order_id)
    return {"msg": translate("order_force_cancelled")}

@router.post("/orders/{order_id}/force_complete")
def force_complete(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    force_complete_order(db, order_id)
    return {"msg": translate("order_force_completed")}

@router.post("/orders/{order_id}/manual_transfer")
def manual_transfer(order_id: int, to_courier_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    manual_transfer_order(db, order_id, to_courier_id)
    return {"msg": translate("order_manually_transferred")}