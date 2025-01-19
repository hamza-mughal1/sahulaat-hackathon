from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.users_db_schema import Users
from schemas.db_schemas.sensors_data_db_schema import SensorsData
from schemas.db_schemas.states_db_schema import States
from schemas.db_schemas.notifications_db_schema import Notifications
from schemas.pydantic_schemas.users_pydantic_schema import CreateUser
from utilities.utils import create_hashed_password


class UsersModel:
    def __init__(self):
        pass

    async def create_user(self, user_data: CreateUser, db: AsyncSession):

        data = user_data.model_dump()
        existing_user = await db.execute(
            select(Users).where(Users.username == data["username"])
        )
        if existing_user.scalars().first():
            return {"message": "user already exists!"}
        data.update(password=create_hashed_password(data["password"]))
        user = Users(**data)
        db.add(user)
        await db.commit()
        

        return {"message": "user has been created!"}
