from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base
# Users Table
class States(Base):
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("sensors_data.id"), nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    pattern_id = Column(Integer, ForeignKey("patterns.id"), nullable=False)
    confident = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    sensors = relationship("Sensors", back_populates="states")
    sensors_data = relationship("SensorsData", back_populates="states")
    patterns = relationship("Patterns", back_populates="states")