from sqlalchemy import Column, ForeignKey, Integer, DateTime, func, Float
from sqlalchemy.orm import relationship
from engines.sql_engine import Base

# Users Table
class SensorsData(Base):
    __tablename__ = "sensors_data"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)    
    flow_rate = Column(Float, nullable=False)
    energy = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    sensors = relationship("Sensors", back_populates="sensors_data")
    patterns = relationship("Patterns", back_populates="sensors_data", cascade="all, delete-orphan")
    states = relationship("States", back_populates="sensors_data", cascade="all, delete-orphan")
    notifications = relationship("Notifications", back_populates="sensors_data", cascade="all, delete-orphan")