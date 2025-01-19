from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.notifications_db_schema import Notifications

class NotificationsModel:
    def __init__(self):
        pass

    async def get_notifications(self, token, db: AsyncSession):
        
        sensors = await db.execute(
            select(Notifications).where(Notifications.user_id == token["user_id"])
        )
        
        sensors = sensors.scalars()
        sensors_list = [sensor for sensor in sensors]
        
        return sensors_list