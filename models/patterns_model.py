from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.patterns_db_schema import Patterns
from schemas.db_schemas.sensors_db_schema import Sensors
from schemas.db_schemas.sensors_data_db_schema import SensorsData
from schemas.pydantic_schemas import pattern_pydantic_schema as pattern_schema
from fastapi import HTTPException


class PatternsModel:
    def __init__(self):
        pass

    async def create_pattern(self, pattern_data: pattern_schema.CreatePattern, token, db: AsyncSession):

        data = pattern_data.model_dump()
        check_for_user = await db.execute(
            select(Sensors).where(and_(Sensors.user_id == token["user_id"]),(Sensors.id == data["sensor_id"]))
        )
        check_for_sensor = await db.execute(
            select(SensorsData).where(and_(SensorsData.id == data["sensor_id"]),(SensorsData.sensor_id == data["record_id"]))
        )
        if (not check_for_user.scalars().first()) and (not check_for_sensor.scalars().first()):
            raise HTTPException(status_code=404, detail="Sensor or Record not found!")
        
        pattern = Patterns(**data)
        db.add(pattern)
        await db.commit()
        

        return {"message": "pattern has been created!"}

    async def get_patterns(self, token, db: AsyncSession):
        print(token["user_id"])
        patterns = await db.execute(
            select(Patterns, Sensors).join(Sensors, Patterns.sensor_id == Sensors.id).where(Sensors.user_id == token["user_id"])
        )
        result = patterns.all()  # Get all rows, each as a tuple (Patterns, Sensors)
        
        if not result:
            raise HTTPException(status_code=404, detail="No patterns found for the given user id!")
        
        # Process result if needed
        combined_data = [(pattern, sensor) for pattern, sensor in result]
        return combined_data