from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.payments import refund_payment, partial_refund
from app.crud.payments import get_all_transactions, get_failed_payments

router = APIRouter()

@router.post("/refund/{payment_id}")
def refund(payment_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role not in ["admin", "support"]:
        raise HTTPException(403)
    refund_payment(db, payment_id)
    return {"msg": "Refunded"}

@router.post("/partial_refund/{payment_id}")
def partial(payment_id: int, amount: float, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role not in ["admin", "support"]:
        raise HTTPException(403)
    partial_refund(db, payment_id, amount)
    return {"msg": "Partial refunded"}

@router.get("/transactions")
def transactions(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    trans = get_all_transactions(db)
    return trans

@router.get("/failed")
def failed(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    fails = get_failed_payments(db)
    return fails