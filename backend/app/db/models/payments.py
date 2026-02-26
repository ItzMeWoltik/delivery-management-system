from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum as SQLEnum
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float)
    status = Column(SQLEnum("pending", "paid", "failed", "refunded", name="payment_status"))