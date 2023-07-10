from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .documents import Document, DriverLicense, Insurance
    from .cars import Car


class User(Base):
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True
    )
    full_name: Mapped[str | None] = mapped_column(String(255), index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    driver_license: Mapped["DriverLicense"] = relationship(
        back_populates="user", cascade="all, delete"
    )
    insurance: Mapped[list["Insurance"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    documents: Mapped[list["Document"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    cars: Mapped[list["Car"]] = relationship(
        back_populates="owner", cascade="all, delete", passive_deletes=True
    )

    def __repr__(self):
        return (
            f"User: id={self.id}, username={self.full_name}, "
            f"email={self.email}"
        )
