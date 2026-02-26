from sqlalchemy.orm import Session
from app.db.models.payments import Payment
from .base import CRUDBase

class CRUDPayment(CRUDBase[Payment]):
    def get_all_transactions(self, db: Session):
        return db.query(Payment).all()

    def get_failed(self, db: Session):
        return db.query(Payment).filter(Payment.status == "failed").all()

payment = CRUDPayment(Payment)
get_all_transactions = payment.get_all_transactions
get_failed_payments = payment.get_failed