from fastapi import APIRouter

from app.db.api import router as db_api
from app.sicavs.api import router as sicavs_api

api_router = APIRouter()

api_router.include_router(sicavs_api, prefix="/sicavs", tags=["Sicavs"])

api_router.include_router(db_api, prefix="/db", tags=["db"])
