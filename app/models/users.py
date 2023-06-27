from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
)

from app.db.base_class import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    car_id = Column(Integer, nullable=True)
    driver_license_id = Column(Integer, nullable=True)
    insurance_id = Column(Integer, nullable=True)
    document_id = Column(Integer, nullable=True)
