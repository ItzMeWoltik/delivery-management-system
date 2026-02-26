from sqlalchemy.orm import Session
from app.db.models.orders import Order
from .base import CRUDBase

class CRUDOrder(CRUDBase[Order]):
    def get_available(self, db: Session):
        return db.query(Order).filter(Order.status == "pending").all()

    def get_active(self, db: Session, courier_id: int):
        return db.query(Order).filter(Order.courier_id == courier_id, Order.status.in_(["accepted", "in_transit"])).all()

    def get_history(self, db: Session, user_id: int):
        return db.query(Order).filter((Order.user_id == user_id) | (Order.courier_id == user_id)).all()

    def get_all(self, db: Session):
        return db.query(Order).all()

    def get_user_orders(self, db: Session, user_id: int):
        return db.query(Order).filter(Order.user_id == user_id).all()

order = CRUDOrder(Order)
get_available_orders = order.get_available
get_active_orders = order.get_active
get_order_history = order.get_history
get_all_orders = order.get_all
get_user_orders = order.get_user_orders