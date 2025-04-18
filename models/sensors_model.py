from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.sensors_db_schema import Sensors
from schemas.db_schemas.sensors_data_db_schema import SensorsData
from schemas.db_schemas.patterns_db_schema import Patterns
from schemas.pydantic_schemas.sensor_pydantic_schema import CreateSensor
from schemas.db_schemas.states_db_schema import States

class SensorsModel:
    def __init__(self):
        pass

    async def add_sensor(self, sensor_data: CreateSensor, token, db: AsyncSession):
        data = sensor_data.model_dump()
        sensor = Sensors(**data, user_id=token["user_id"])
        db.add(sensor)
        await db.commit()
        
        return {"device_name":sensor.name, "secret_key": sensor.secret_key}

    async def get_sensors(self, token, db: AsyncSession):
        
        sensors = await db.execute(
            select(Sensors).where(Sensors.user_id == token["user_id"])
        )
        
        sensors = sensors.scalars()
        sensors_list = [sensor for sensor in sensors]
        
        return sensors_list
    
    async def get_sensor_state(self, sensor_id, token, db: AsyncSession):

        sensors = await db.execute(
            select(Sensors).where(and_(Sensors.user_id == token["user_id"], Sensors.id == sensor_id))
        )
        
        data = sensors.scalars().first()
        if not data:
            return HTTPException(status_code=404, detail="Sensor not found")
        
        state = await db.execute(
            select(States).where(States.sensor_id == sensor_id)
        )
        
        state = state.scalars().first()
        
        if not state:
            return HTTPException(status_code=404, detail="No data available")
        
        sensors_data = await db.execute(
            select(SensorsData).where(SensorsData.id == state.record_id)
        )
        
        sensors_data = sensors_data.scalars().first()
        
        sensor = await db.execute(
            select(Sensors).where(Sensors.id == state.sensor_id)
        )
        
        sensor = sensor.scalars().first()
        
        pattern = await db.execute(
            select(Patterns).where(Patterns.id == state.pattern_id)
        )
        
        pattern = pattern.scalars().first()
        
        output_data = {"confident": state.confident,
                       "flow_rate": sensors_data.flow_rate,
                       "energy": sensors_data.energy,
                       "pressure": sensors_data.pressure,
                       "temperature": sensors_data.temperature,
                       "sensor_name": sensor.name,
                       "pattern_name": pattern.name
                       }
        
        return output_data
        
        # sensor = sensor.scalars().first()
        
        # sensor_data = await db.execute(
        #     select(SensorsData).where(SensorsData.sensor_id == sensor_id)
        # )
        
        # sensor_data = sensor_data.scalars()
        # sensor_data_list = [data for data in sensor_data]
        
        # return sensor, sensor_data_list