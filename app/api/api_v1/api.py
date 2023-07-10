from fastapi import APIRouter, Depends

from app.db.session import get_async_session
from .endpoints import engines

api_router = APIRouter()

api_router.include_router(
    engines.router,
    prefix="/engines",
    tags=["Engines"],
    dependencies=[Depends(get_async_session)],
)
