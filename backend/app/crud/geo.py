from sqlalchemy.orm import Session
from app.db.models.geo import Location
from .base import CRUDBase

class CRUDLocation(CRUDBase[Location]):
    def get_history(self, db: Session, courier_id: int):
        return db.query(Location).filter(Location.courier_id == courier_id).order_by(Location.timestamp).all()

location = CRUDLocation(Location)
get_location_history = location.get_history