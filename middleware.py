import json
from pathlib import Path
from fastapi import HTTPException, Request, status
import re
from engines.sql_engine import AsyncSessionLocal
from jose import jwt, JWTError
from sqlalchemy.future import select
from schemas.db_schemas import users_db_schema
from utilities.settings import setting
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

# AuthenticationMiddware class for managing token middware. (child class of starlette middleware class)
class AuthenticationMiddleware(BaseHTTPMiddleware):

    # function to get token from the request's cookies and check if it is a valid JWT token
    @staticmethod
    async def get_token(request: Request):
        """extracts token from the request's cookies and checks if it is a valid JWT token using regex

        Args:
            request (Request): FastAPI request object

        Raises:
            HTTPException: (HTTP_401_UNAUTHORIZED, "Invalid or missing token") if token is in the cookies or if it doesn't start with 'Bearer '
            HTTPException: (HTTP_401_UNAUTHORIZED, "Malformed or invalid token") if token doesn't match regex of JWT

        Returns:
            token (Str): Token extracted from the cookies
        """
        # get the token from cookies with key 'access_token'
        authorization = request.cookies.get("access_token")
        # if token is present in the cookies then raise the error
        if authorization is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
            )
        # Check if the Authorization header starts with "Bearer "
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
            )

        # Extract the token part
        token = authorization.split("Bearer ")[1]

        # Define a regex pattern for a valid token
        token_pattern = r"^[A-Za-z0-9\-_]+\.([A-Za-z0-9\-_]+)?\.([A-Za-z0-9\-_]+)?$"  # Basic JWT structure

        # Check if the token matches the regex
        if not re.match(token_pattern, token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Malformed or invalid token",
            )

        return token

    # function to verify if the token was signed by us and hasn't expired yet
    @staticmethod
    async def verify_token(db, token, SECRET_KEY, ALGORITHM):

        try:
            # decode the token with given secret key and algorithm. Returns dict
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_id = payload.get("user_id")
            user_name = payload.get("user_name")

            # if user_id and user_name is not in the token then raise the error. Because it is an invalid token
            if (user_id is None) or (user_name is None):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="token is invalid",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # fetching user from the DB using it's id got from the token's payload
            result = await db.execute(
                select(users_db_schema.Users).where(users_db_schema.Users.id == user_id)
            )

            # if the user doesn't exist in the DB then raise teh error
            if (result.scalar_one_or_none()) is None:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token. (User not found)",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # if anything goes wrong while decoding the token. If the token is invalid or expired then raise the error
        except JWTError:
            raise HTTPException(
                status_code=403,
                detail="token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # return given JWT token's payload
        return payload

    # function to control main middlware flow. Don't change the name
    async def dispatch(self, request: Request, call_next):

        # Check if the request path is in the excluded endpoints
        excluded_endpoints = config_data.get("excluded_endpoints", [])
        if (request.url.path in excluded_endpoints) or (
            request.url.path + "/" in excluded_endpoints
        ):
            # if request path is in the excluded endpoints then directly transfer the request to the endpoint
            return await call_next(request)

        secret_key = setting.secret
        algorithm = setting.algorithm
        try:
            # get the token from the cookies
            token = await AuthenticationMiddleware.get_token(request)
            # start async DB session
            async with AsyncSessionLocal() as db:
                # verify token
                payload = await AuthenticationMiddleware.verify_token(
                    db, token, secret_key, algorithm
                )

            # if if the user role is allowed
            await AuthenticationMiddleware.check_access(request, payload)
            # transfer the request to the endpoint
            return await call_next(request)
        except Exception as e:
            try:
                # return the error back to the FastAPI as JSON response with same status code and detail. Because FastAPI doesn't allow
                # HTTPException in middlware so has to direct it this way.
                return JSONResponse(status_code=e.status_code, content=e.detail)
            except:
                # if the error doesn't have status code and detail then raise it because it is an internal server error
                raise e
