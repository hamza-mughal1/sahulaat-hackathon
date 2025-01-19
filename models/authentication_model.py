from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Response, Request
from schemas.db_schemas import users_db_schema
from utilities.utils import verify_password
from utilities.settings import setting
from sqlalchemy.future import select
import uuid
from utilities.dependencies import db_dependency

class Authentication:
    def __init__(
        self,
        secret_key=setting.secret,
        algorithm=setting.algorithm,
        access_token_expire_minutes=setting.access_token_expire_minutes,
        refresh_token_expire_minutes=setting.refresh_token_expire_minutes,
    ):
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expire_minutes
        self.REFRESH_TOKEN_EXPIRE_MINUTES = refresh_token_expire_minutes

    async def create_token(self, data: dict, refresh=False):
        to_encode = data.copy()
        if refresh:
            expiration = datetime.now() + timedelta(
                minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        else:
            expiration = datetime.now() + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": round(expiration.timestamp())})
        to_encode.update({"uuid": str(uuid.uuid4())})

        ecoded_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return ecoded_token

    async def get_token_websockets(self, headers):
        authorization: str = headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Invalid or missing token")
        token = authorization.split("Bearer ")[1]
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        return payload

    async def get_token(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Invalid or missing token")
        token = authorization.split("Bearer ")[1]
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        return payload

    async def login(self, user_credentials, db: db_dependency):
        result = await db.execute(
            select(users_db_schema.Users).where(
                users_db_schema.Users.username == user_credentials.username
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=403, detail="Invalid Credentials")
        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=403, detail="Invalid Credentials")

        access_token = await self.create_token(
            {"user_id": user.id, "user_name": user.username, "type": "access-token"}
        )

        # response.set_cookie(
        #     key="access_token",
        #     value=f"Bearer {access_token}",
        #     httponly=True,  # Prevent JavaScript access to the cookie
        #     secure=True,  # Use Secure cookies (HTTPS only)
        #     samesite="Lax",  # Prevent CSRF attacks
        #     max_age=self.ACCESS_TOKEN_EXPIRE_MINUTES
        #     * 60,  # Set cookie expiry in seconds
        #     path="/"         ## for a specific path
        # )

        return {"message": "Login successful", "token": access_token}