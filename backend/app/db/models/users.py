from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SQLEnum("customer", "courier", "admin", "support", name="roles"))
    is_active = Column(Boolean, default=True)