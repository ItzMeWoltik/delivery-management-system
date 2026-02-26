from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    courier_id = Column(Integer, ForeignKey("users.id"))
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)