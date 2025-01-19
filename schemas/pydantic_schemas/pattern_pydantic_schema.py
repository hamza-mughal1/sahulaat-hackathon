from pydantic import BaseModel

class CreatePattern(BaseModel):
    record_id: int
    sensor_id: int
    name: str