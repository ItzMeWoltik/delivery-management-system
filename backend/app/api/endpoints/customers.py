from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.orders import OrderCreate
from app.services.orders import create_order, get_order_status, cancel_order
from app.services.payments import process_payment, check_payment_status
from app.crud.orders import get_user_orders
from app.core.i18n import translate

router = APIRouter()

@router.post("/orders")
def create_customer_order(order: OrderCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "customer":
        raise HTTPException(403)
    new_order = create_order(db, order, user.id)
    return {"order_id": new_order.id, "msg": translate("order_created")}

@router.get("/orders/{order_id}/status")
def view_order_status(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    status = get_order_status(db, order_id, user.id)
    return {"status": status}

@router.post("/orders/{order_id}/cancel")
def cancel_customer_order(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    cancel_order(db, order_id, user.id)
    return {"msg": translate("order_cancelled")}

@router.post("/orders/{order_id}/pay")
def pay_order(order_id: int, card_details: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    payment_id = process_payment(db, order_id, card_details)
    return {"payment_id": payment_id}

@router.get("/orders/{order_id}/payment/status")
def payment_status(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    status = check_payment_status(db, order_id)
    return {"status": status}

@router.get("/orders/history")
def order_history(db: Session = Depends(get_db), user = Depends(get_current_user)):
    orders = get_user_orders(db, user.id)
    return orders