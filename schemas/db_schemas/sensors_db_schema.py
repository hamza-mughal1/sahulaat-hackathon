from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
# Users Table
class Sensors(Base):
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)    
    name = Column(String, nullable=False)
    secret_key = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    users = relationship("Users", back_populates="sensors")
    sensors_data = relationship("SensorsData", back_populates="sensors", cascade="all, delete-orphan")
    patterns = relationship("Patterns", back_populates="sensors", cascade="all, delete-orphan")
    states = relationship("States", back_populates="sensors", cascade="all, delete-orphan")
    notifications = relationship("Notifications", back_populates="sensors", cascade="all, delete-orphan")