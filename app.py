from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers.users_handler import router as users_router
from handlers.authentication_handler import router as authentication_router
from sqlalchemy.ext.asyncio import AsyncEngine
from engines.sql_engine import Base, engine

# create app
app = FastAPI()

# create tables in the db if don't exist (commented out because using alembic to manage DB migration)
async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# add all routers to app
app.include_router(users_router)
app.include_router(authentication_router)

# check for tables creation on the startup
@app.on_event("startup")
async def on_startup():
    await create_tables(engine)

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
