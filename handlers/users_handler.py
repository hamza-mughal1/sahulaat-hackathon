from fastapi import APIRouter
from schemas.pydantic_schemas import users_pydantic_schema as user_schema
from models.users_model import UsersModel
from utilities.dependencies import db_dependency

# router object to create routes 
router = APIRouter(prefix="/users", tags=["users"])

# user model class object to call it's functions
user = UsersModel()


@router.post("/")
async def create_user(user_data: user_schema.CreateUser, db: db_dependency):
    return await user.create_user(user_data, db)
