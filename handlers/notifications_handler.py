from fastapi import APIRouter
from models.notifications_model import NotificationsModel
from utilities.dependencies import db_dependency, token_dependency

# router object to create routes 
router = APIRouter(prefix="/notifications", tags=["notifications"])

# user model class object to call it's functions
notification = NotificationsModel()


@router.get("/")
async def get_notifications(token: token_dependency, db: db_dependency):
    return await notification.get_notifications(token, db)
