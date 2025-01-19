from sqlalchemy import Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base
# Users Table
class Notifications(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    record_id = Column(Integer, ForeignKey("sensors_data.id"))
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    
    users = relationship("Users", back_populates="notifications")
    sensors = relationship("Sensors", back_populates="notifications")
    sensors_data = relationship("SensorsData", back_populates="notifications")