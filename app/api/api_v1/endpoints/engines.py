from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api import deps
from app.crud import crud_engine
from app.db.session import get_async_session

router = APIRouter()


@router.get("/", response_model=list[schemas.EngineRead])
async def read_engines(
    session: AsyncSession = Depends(get_async_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get list of engines."""
    engines = await crud_engine.get_multi(session)
    return engines


@router.get("/{engine_id}", response_model=schemas.EngineRead)
async def read_engine_by_id(
    engine_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve engine by the ID."""
    engine = await crud_engine.get(session, engine_id)
    if not engine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Engine with id={engine_id} doesn't exist.",
        )
    return engine


@router.post("/", response_model=schemas.EngineRead)
async def create_engine(
    engine_in: schemas.EngineCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create a new engine."""
    engine = await crud_engine.get_by_model(session, model=engine_in.model)
    if engine:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This model of engine already exists."
        )
    engine = await crud_engine.create(session, create_schema=engine_in)
    return engine

