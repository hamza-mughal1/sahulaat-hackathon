from pydantic import BaseModel

class CreateSensor(BaseModel):
    name: str
    
class GetSensor(BaseModel):
    id: int
    name: str
        
class IncomingData(BaseModel):
    secret_key: str
    flow_rate: float
    energy: float
    pressure: float
    temperature: float