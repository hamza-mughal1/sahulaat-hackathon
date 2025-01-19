from sqlalchemy import Column, Integer, DateTime, func
from engines.sql_engine import Base
# Users Table
class DeviceToken(Base):
    __tablename__ = "device_token"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(Integer, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)