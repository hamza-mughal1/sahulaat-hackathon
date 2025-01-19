from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base
# Users Table
class Patterns(Base):
    __tablename__ = "patterns"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("sensors_data.id"), nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    sensors = relationship("Sensors", back_populates="patterns")
    sensors_data = relationship("SensorsData", back_populates="patterns")
    states = relationship("States", back_populates="patterns", cascade="all, delete-orphan")