from fastapi import APIRouter
from schemas.pydantic_schemas import pattern_pydantic_schema as pattern_schema
from models.patterns_model import PatternsModel
from utilities.dependencies import db_dependency, token_dependency

# router object to create routes 
router = APIRouter(prefix="/patterns", tags=["patterns"])

# user model class object to call it's functions
patterns = PatternsModel()


@router.post("/")
async def create_pattern(pattern_data: pattern_schema.CreatePattern, token: token_dependency, db: db_dependency):
    return await patterns.create_pattern(pattern_data, token, db)

@router.get("/")
async def get_patterns(token: token_dependency, db: db_dependency):
    return await patterns.get_patterns(token, db)
