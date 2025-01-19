from fastapi import APIRouter
from schemas.pydantic_schemas import sensor_pydantic_schema as sensor_schema
from models.sensors_model import SensorsModel
from models.authentication_model import Authentication
from typing import List
from utilities.dependencies import db_dependency, token_dependency
from fastapi import WebSocket
import asyncio

# router object to create routes 
router = APIRouter(prefix="/sensors", tags=["sensors"])

# user model class object to call it's functions
sensor = SensorsModel()
authen = Authentication()

@router.get("/", response_model=List[sensor_schema.GetSensor])
async def get_sensors(token: token_dependency, db: db_dependency):
    return await sensor.get_sensors(token, db)


@router.post("/")
async def add_sensor(sensor_data: sensor_schema.CreateSensor, token: token_dependency, db: db_dependency):
    return await sensor.add_sensor(sensor_data, token, db)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, sensor_id: int, db: db_dependency):
    await websocket.accept()
    try:
        headers = websocket.headers
        token = await authen.get_token_websockets(headers)
        
        while True:
            output = await sensor.get_sensor_state(sensor_id, token, db)
            await websocket.send_text(f"output = {output}")
            await asyncio.sleep(2)
    except:
        pass
