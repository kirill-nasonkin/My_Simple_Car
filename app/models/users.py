from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .documents import Document, DriverLicense, Insurance
    from .cars import Car


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    driver_license: Mapped["DriverLicense"] = relationship(
        back_populates="user", cascade="all, delete"
    )
    insurance: Mapped[list["Insurance"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    document: Mapped[list["Document"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    cars: Mapped[list["Car"]] = relationship(
        back_populates="owner", cascade="all, delete", passive_deletes=True
    )

    def __repr__(self):
        return (
            f"User: id={self.id}, username={self.username}, "
            f"email={self.email}"
        )
