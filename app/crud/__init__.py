from app.crud.base import CRUDBase
from app.models import Engine
from app.schemas.engines import EngineCreate, EngineUpdate

from .crud_user import user

crud_engine = CRUDBase[Engine, EngineCreate, EngineUpdate](Engine)
