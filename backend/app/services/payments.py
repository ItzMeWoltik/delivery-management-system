from sqlalchemy.orm import Session
from app.db.models.orders import Order
from app.db.models.payments import Payment

class MockStripe:
    def charge(self, amount, card):
        return "paid" if 'number' in card else "failed"

    def refund(self, payment_id, amount=None):
        return "refunded"

mock_stripe = MockStripe()

def process_payment(db: Session, order_id: int, card_details: dict):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")
    payment = Payment(order_id=order_id, amount=order.cost, status="pending")
    db.add(payment)
    db.commit()
    db.refresh(payment)
    status = mock_stripe.charge(payment.amount, card_details)
    payment.status = status
    db.commit()
    return payment.id

def check_payment_status(db: Session, order_id: int):
    payment = db.query(Payment).filter(Payment.order_id == order_id).first()
    return payment.status if payment else "no_payment"

def refund_payment(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise ValueError("Payment not found")
    mock_stripe.refund(payment_id)
    payment.status = "refunded"
    db.commit()

def partial_refund(db: Session, payment_id: int, amount: float):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise ValueError("Payment not found")
    mock_stripe.refund(payment_id, amount)
    payment.amount -= amount
    db.commit()