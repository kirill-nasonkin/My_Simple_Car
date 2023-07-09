from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.crud import crud_engine
from app.db.session import async_session_maker, get_async_session

router = APIRouter()


@router.get("/")
async def get_engines(
    session: AsyncSession = Depends(get_async_session),
) -> list[schemas.EngineRead | None]:
    # async with async_session_maker() as session:
    engines = await crud_engine.get_multi(session)
    return engines
