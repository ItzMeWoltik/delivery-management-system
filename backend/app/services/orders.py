from enum import Enum
from sqlalchemy.orm import Session
from app.db.models.orders import Order
from app.services.geo import calculate_distance
from threading import Timer
from datetime import timedelta
from app.utils.logging import log_action
from app.services.notifications import send_notification

class OrderState(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

allowed_transitions = {
    OrderState.PENDING: [OrderState.ACCEPTED, OrderState.CANCELLED],
    OrderState.ACCEPTED: [OrderState.IN_TRANSIT, OrderState.CANCELLED],
    OrderState.IN_TRANSIT: [OrderState.COMPLETED, OrderState.CANCELLED],
    OrderState.COMPLETED: [],
    OrderState.CANCELLED: [],
}

def validate_transition(current: str, next_state: str):
    if OrderState(next_state) not in allowed_transitions.get(OrderState(current), []):
        raise ValueError("Invalid state transition")

def create_order(db: Session, order_data: dict, user_id: int):
    dist = calculate_distance(order_data['from_address'], order_data['to_address'])
    cost = 5 + dist * 0.5
    order = Order(user_id=user_id, from_address=order_data['from_address'], to_address=order_data['to_address'], cost=cost, status=OrderState.PENDING.value)
    db.add(order)
    db.commit()
    db.refresh(order)
    log_action(f"Order created: {order.id}")
    return order

def get_order_status(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or (order.user_id != user_id and order.courier_id != user_id):
        raise ValueError("Access denied")
    return order.status

def cancel_order(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order.user_id != user_id:
        raise ValueError("Access denied")
    validate_transition(order.status, OrderState.CANCELLED.value)
    order.status = OrderState.CANCELLED.value
    db.commit()
    log_action(f"Order cancelled: {order_id}")
    Timer(86400, alert_admin_if_not_returned, args=(db, order_id)).start()

def alert_admin_if_not_returned(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order and order.status == OrderState.CANCELLED.value:
        send_notification("admin", f"Order {order_id} not returned")

def accept_order(db: Session, order_id: int, courier_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.status == "pending").first()
    if not order:
        raise ValueError("Order not available")
    order.courier_id = courier_id
    order.status = OrderState.ACCEPTED.value
    db.commit()

def decline_order(db: Session, order_id: int, courier_id: int):
    # Logic to decline, perhaps log for pause calculation
    pass

def start_delivery(db: Session, order_id: int, courier_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.courier_id == courier_id).first()
    if not order:
        raise ValueError("Access denied")
    validate_transition(order.status, OrderState.IN_TRANSIT.value)
    order.status = OrderState.IN_TRANSIT.value
    db.commit()

def complete_delivery(db: Session, order_id: int, courier_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.courier_id == courier_id).first()
    if not order:
        raise ValueError("Access denied")
    validate_transition(order.status, OrderState.COMPLETED.value)
    order.status = OrderState.COMPLETED.value
    db.commit()

def transfer_order(db: Session, order_id: int, from_courier_id: int, to_courier_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.courier_id == from_courier_id).first()
    if not order:
        raise ValueError("Access denied")
    order.courier_id = to_courier_id
    db.commit()

def force_cancel_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    order.status = OrderState.CANCELLED.value
    db.commit()

def force_complete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    order.status = OrderState.COMPLETED.value
    db.commit()

def manual_transfer_order(db: Session, order_id: int, to_courier_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    order.courier_id = to_courier_id
    db.commit()