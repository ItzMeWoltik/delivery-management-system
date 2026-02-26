from sqlalchemy.orm import Session
from app.db.models.geo import Location
from app.services.geo import calculate_distance
from app.services.notifications import send_notification

def detect_fraud(db: Session, courier_id: int):
    locations = db.query(Location).filter(Location.courier_id == courier_id).order_by(Location.timestamp).all()
    if len(locations) < 2:
        return False
    for i in range(1, len(locations)):
        prev = locations[i-1]
        curr = locations[i]
        dist = calculate_distance(f"{prev.lat},{prev.lon}", f"{curr.lat},{curr.lon}")
        time_diff = (curr.timestamp - prev.timestamp).total_seconds() / 3600
        speed = dist / time_diff if time_diff > 0 else 0
        if speed > 100 or dist > 5:
            send_notification("admin", f"Fraud detected for courier {courier_id}")
            return True
    return False

def get_fraud_alerts(db: Session):
    # Mock or query actual alerts
    return [{"courier_id": 1, "type": "speed_violation", "date": "2023-01-01"}]