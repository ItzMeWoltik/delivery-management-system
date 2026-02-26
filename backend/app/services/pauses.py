from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.base import Base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey

class Pause(Base):
    __tablename__ = "pauses"
    id = Column(Integer, primary_key=True)
    courier_id = Column(Integer, ForeignKey("users.id"))
    duration = Column(Float)  # hours
    reason = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)

class Violation(Base):
    __tablename__ = "violations"
    id = Column(Integer, primary_key=True)
    courier_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

violation_levels = [0.5, 2, 24]  # hours

def apply_pause(db: Session, courier_id: int, duration: float, reason: str):
    pause = Pause(courier_id=courier_id, duration=duration, reason=reason)
    db.add(pause)
    db.commit()

def check_pause_status(db: Session, courier_id: int):
    pause = db.query(Pause).filter(Pause.courier_id == courier_id).order_by(Pause.start_time.desc()).first()
    if pause:
        end_time = pause.start_time + timedelta(hours=pause.duration)
        if datetime.utcnow() < end_time:
            return True
    return False