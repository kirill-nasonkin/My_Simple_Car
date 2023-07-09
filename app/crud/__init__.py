from app.crud.base import CRUDBase
from app.models import Car, Engine, Image
from app.schemas.engines import EngineCreate, EngineUpdate

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
crud_image = CRUDBase(Image)
crud_car = CRUDBase(Car)
crud_engine = CRUDBase[Engine, EngineCreate, EngineUpdate](Engine)
