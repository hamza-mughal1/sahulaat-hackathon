from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers.users_handler import router as users_router
from handlers.authentication_handler import router as authentication_router
from handlers.patterns_handler import router as patterns_router
from handlers.sensors_handlers import router as sensor_router
from handlers.notifications_handler import router as notifications_router
from sqlalchemy.ext.asyncio import AsyncEngine
from engines.sql_engine import Base, engine
from mqtt.subs_testing import run_mqtt_consumer
import asyncio

# create app
app = FastAPI()

# create tables in the db if don't exist (commented out because using alembic to manage DB migration)
async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# add all routers to app
app.include_router(users_router)
app.include_router(authentication_router)
app.include_router(sensor_router)
app.include_router(patterns_router)
app.include_router(notifications_router)


# check for tables creation on the startup
@app.on_event("startup")
async def on_startup():
    await create_tables(engine)
    asyncio.create_task(run_mqtt_consumer())

# configure CORS middleware (allowed to everyone for now)
origins = ["*"]


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "Hello from sahulaat!"
