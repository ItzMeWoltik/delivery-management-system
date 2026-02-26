from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum
from datetime import datetime
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    from_address = Column(String)
    to_address = Column(String)
    cost = Column(Float)
    status = Column(SQLEnum("pending", "accepted", "in_transit", "completed", "cancelled", name="order_status"), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderLog(Base):
    __tablename__ = "order_logs"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)