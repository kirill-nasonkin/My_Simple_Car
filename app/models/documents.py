from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User


class BaseDocument:
    start_date: Mapped[datetime]
    exp_date: Mapped[datetime]


class DriverLicense(Base, BaseDocument):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="driver_license")

    def __repr__(self):
        return (
            f"Driver License: id={self.id}, {self.start_date} - "
            f"{self.exp_date}"
        )


class Insurance(Base, BaseDocument):
    insurer: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="insurance")

    def __repr__(self):
        return (
            f"Insurance: id={self.id}, {self.start_date} - {self.exp_date}, "
            f"insurer={self.insurer}"
        )


class Document(Base, BaseDocument):
    title: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="documents")

    def __repr__(self):
        return (
            f"Document: id={self.id}, title={self.title}, {self.start_date} - "
            f"{self.exp_date}"
        )
