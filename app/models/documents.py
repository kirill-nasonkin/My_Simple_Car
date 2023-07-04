from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401


class BaseDocument:
    start_date: Mapped[datetime]
    exp_date: Mapped[datetime]


class DriverLicense(Base, BaseDocument):
    user: Mapped["User"] = relationship(back_populates="driver_license")


class Insurance(Base, BaseDocument):
    insurer: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="insurance")


class Document(Base, BaseDocument):
    title: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="document")
