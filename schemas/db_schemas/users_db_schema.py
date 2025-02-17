from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base
# Users Table
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    sensors = relationship("Sensors", back_populates="users", cascade="all, delete-orphan")
    notifications = relationship("Notifications", back_populates="users", cascade="all, delete-orphan")
    