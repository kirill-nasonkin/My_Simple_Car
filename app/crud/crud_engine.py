from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Engine
from app.schemas import EngineCreate, EngineUpdate


class CRUDEngine(CRUDBase[Engine, EngineCreate, EngineUpdate]):
    @staticmethod
    async def get_by_model(
        session: AsyncSession, *, model: str
    ) -> Engine | None:
        statement = select(Engine).where(Engine.model == model)
        results = await session.execute(statement)
        return results.scalar_one_or_none()


crud_engine = CRUDEngine(Engine)
