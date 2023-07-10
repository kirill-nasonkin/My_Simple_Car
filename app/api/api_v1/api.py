from fastapi import APIRouter

from .endpoints import engines, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(engines.router, prefix="/engines", tags=["Engines"])
