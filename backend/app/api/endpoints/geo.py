from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.geo import get_location_history, get_route
from app.services.fraud import detect_fraud

router = APIRouter()

@router.get("/couriers/{courier_id}/locations")
def locations(courier_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    history = get_location_history(db, courier_id)
    return history

@router.get("/couriers/{courier_id}/route")
def route(courier_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    route = get_route(db, courier_id)
    return route

@router.post("/fraud/check/{courier_id}")
def check_fraud(courier_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    fraud = detect_fraud(db, courier_id)
    return {"fraud_detected": fraud}