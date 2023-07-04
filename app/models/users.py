from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .documents import Document, DriverLicense, Insurance  # noqa: F401
    from .cars import Car


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    car_id: Mapped[Optional[int]] = mapped_column(ForeignKey("car.id"))
    driver_license_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("driverlicense.id")
    )
    insurance_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("insurance.id")
    )
    document_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("document.id")
    )

    driver_license: Mapped["DriverLicense"] = relationship(
        back_populates="user"
    )
    insurance: Mapped[List["Insurance"]] = relationship(back_populates="user")
    document: Mapped[List["Document"]] = relationship(back_populates="user")
    cars: Mapped[List["Car"]] = relationship(back_populates="owner")
