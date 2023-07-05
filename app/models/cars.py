from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

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
    car: Mapped["Car"] = relationship(back_populates="avatar")

    def __repr__(self):
        return f"Image: {self.title}, {self.file[:15]}"


class Body(Base):
    title: Mapped[str] = mapped_column(String(255), unique=True)
    image_id: Mapped[Image] = mapped_column(ForeignKey("image.id"))

    cars: Mapped[List["Car"]] = relationship("Car", back_populates="body")
    image: Mapped["Image"] = relationship("Image", back_populates="body")

    def __repr__(self):
        return f"Body: {self.title}, {self.image!r}"


class Engine(Base):
    model: Mapped[str] = mapped_column(String(255), unique=True)
    fuel_type: Mapped[str] = mapped_column(String(255))
    volume: Mapped[float] = mapped_column(Float(1))
    power: Mapped[Optional[int]] = mapped_column(default=volume * 68)

    cars: Mapped[List["Car"]] = relationship("Car", back_populates="engine")

    def __repr__(self):
        return (
            f"Engine: {self.model}, {self.fuel_type}, "
            f"{self.volume:.1f}, {self.power}"
        )


class Maintenance(Base):
    title: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    current_car_mileage: Mapped[int]
    maintenance_interval: Mapped[int]
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))

    car: Mapped["Car"] = relationship("Car", back_populates="maintenances")

    def __repr__(self):
        return f"Maintenance: {self.title}, {self.date}. Car: {self.car!r}"


class Car(Base):
    image_id: Mapped[Optional[int]] = mapped_column(ForeignKey("image.id"))
    vin: Mapped[str] = mapped_column(String(17), unique=True)
    year_built: Mapped[int]
    brand: Mapped[str] = mapped_column(String(255))
    model: Mapped[str] = mapped_column(String(255))
    mileage: Mapped[int]
    avg_month_mil: Mapped[int] = mapped_column(default=400)
    gearbox: Mapped[str] = mapped_column(String(255))  # мкпп \ акпп \ ...
    body_id: Mapped[int] = mapped_column(ForeignKey("body.id"))
    engine_id: Mapped[int] = mapped_column(ForeignKey("engine.id"))

    avatar: Mapped["Image"] = relationship(back_populates="car")
    body: Mapped["Body"] = relationship(back_populates="cars")
    engine: Mapped["Engine"] = relationship(back_populates="cars")
    maintenances: Mapped[List["Maintenance"]] = relationship(
        back_populates="car"
    )
    owner: Mapped["User"] = relationship(back_populates="cars")

    def __repr__(self):
        return f"Car: {self.brand}-{self.model}. Owner: {self.owner!r}"
