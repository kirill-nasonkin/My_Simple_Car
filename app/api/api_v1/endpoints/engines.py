from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.crud import crud_engine
from app.db.session import get_async_session

router = APIRouter()


@router.get("/")
async def get_engines(
    session: AsyncSession = Depends(get_async_session),
) -> list[schemas.EngineRead | None]:
    engines = await crud_engine.get_multi(session)
    return engines
