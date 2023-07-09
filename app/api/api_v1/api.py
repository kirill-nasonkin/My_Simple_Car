from fastapi import APIRouter, Depends

from .endpoints import engines
from ...db.session import get_async_session

api_router = APIRouter()

api_router.include_router(
    engines.router,
    prefix="/engines",
    tags=["Engines"],
    dependencies=[Depends(get_async_session)],
)
