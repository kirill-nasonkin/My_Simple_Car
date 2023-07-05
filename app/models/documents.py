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

    def __repr__(self):
        return (
            f"DriverLicense: {self.start_date} - {self.exp_date}. "
            f"Driver: {self.user!r}"
        )


class Insurance(Base, BaseDocument):
    insurer: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="insurance")

    def __repr__(self):
        return (
            f"Insurance: {self.start_date} - {self.exp_date}. "
            f"Insurer: {self.insurer} "
            f"Driver: {self.user!r}"
        )


class Document(Base, BaseDocument):
    title: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="document")

    def __repr__(self):
        return (
            f"Document: {self.title}, {self.start_date} - {self.exp_date}. "
            f"Driver: {self.user!r}"
        )
