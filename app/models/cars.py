from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings import settings
from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401


class Image(Base):
    title: Mapped[str] = mapped_column(String(255), unique=True)
    file: Mapped[str] = mapped_column(
        FileType(storage=FileSystemStorage(path=settings.STORAGE))
    )

    body: Mapped["Body"] = relationship(back_populates="image")
    car: Mapped["Car"] = relationship(back_populates="image")

    def __repr__(self):
        return f"Image: title={self.title}, path={self.file}"


class Body(Base):
    image_id: Mapped[int] = mapped_column(ForeignKey("image.id"))

    title: Mapped[str] = mapped_column(String(255), unique=True)

    cars: Mapped[list["Car"]] = relationship("Car", back_populates="body")
    image: Mapped["Image"] = relationship("Image", back_populates="body")

    def __repr__(self):
        return f"Body: id={self.id}, title={self.title}"


class Engine(Base):
    model: Mapped[str] = mapped_column(String(255), unique=True)
    fuel_type: Mapped[str] = mapped_column(String(255))
    volume: Mapped[float] = mapped_column(Float(1))
    power: Mapped[int | None]

    cars: Mapped[list["Car"]] = relationship("Car", back_populates="engine")

    def __repr__(self):
        return (
            f"Engine: id={self.id}, model={self.model}, "
            f"fuel_type={self.fuel_type}, "
            f"volume={self.volume:.1f}, power={self.power}"
        )


class Maintenance(Base):
    car_id: Mapped[int] = mapped_column(
        ForeignKey("car.id", ondelete="CASCADE")
    )

    title: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    current_car_mileage: Mapped[int]
    maintenance_interval: Mapped[int]

    car: Mapped["Car"] = relationship("Car", back_populates="maintenances")

    def __repr__(self):
        return (
            f"Maintenance: id={self.id}, title={self.title}, "
            f"date={self.date}"
        )


class Car(Base):
    image_id: Mapped[int | None] = mapped_column(ForeignKey("image.id"))
    body_id: Mapped[int] = mapped_column(ForeignKey("body.id"))
    engine_id: Mapped[int] = mapped_column(ForeignKey("engine.id"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    vin: Mapped[str] = mapped_column(String(17), unique=True)
    year_built: Mapped[int]
    brand: Mapped[str] = mapped_column(String(255))
    model: Mapped[str] = mapped_column(String(255))
    mileage: Mapped[int]
    avg_month_mileage: Mapped[int] = mapped_column(default=400)
    gearbox: Mapped[str] = mapped_column(String(255))

    image: Mapped["Image"] = relationship(back_populates="car")
    body: Mapped["Body"] = relationship(back_populates="cars")
    engine: Mapped["Engine"] = relationship(back_populates="cars")
    maintenances: Mapped[list["Maintenance"]] = relationship(
        back_populates="car", cascade="all, delete"
    )
    owner: Mapped["User"] = relationship(back_populates="cars")

    def __repr__(self):
        return (
            f"Car: id={self.id}, brand={self.brand}, model={self.model} "
            f"vin={self.vin}"
        )
