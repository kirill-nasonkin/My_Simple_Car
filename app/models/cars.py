from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401


class Body(Base):
    title: Mapped[str] = mapped_column(String(255), unique=True)
    default_body_avatar: Mapped[str] = mapped_column(String(255), unique=True)

    cars: Mapped[List["Car"]] = relationship("Car", back_populates="body")


class Engine(Base):
    model: Mapped[str] = mapped_column(String(255), unique=True)
    fuel_type: Mapped[str] = mapped_column(String(255))
    volume: Mapped[float] = mapped_column(Float(1))
    power: Mapped[Optional[int]] = mapped_column(default=volume * 68)

    cars: Mapped[List["Car"]] = relationship("Car", back_populates="engine")

    def __repr__(self):
        return f"Engine: {self.model} - {self.fuel_type} - {self.volume}"


class Maintenance(Base):
    title: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    current_car_mileage: Mapped[int]
    maintenance_interval: Mapped[int]
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))

    car: Mapped["Car"] = relationship("Car", back_populates="maintenances")


class Car(Base):
    avatar: Mapped[str] = mapped_column(String(255))
    vin: Mapped[str] = mapped_column(String(17), unique=True)
    year_built: Mapped[int]
    brand: Mapped[str] = mapped_column(String(255))
    model: Mapped[str] = mapped_column(String(255))
    mileage: Mapped[int]
    avg_month_mil: Mapped[int] = mapped_column(default=400)
    gearbox: Mapped[str] = mapped_column(String(255))  # мкпп \ акпп \ ...
    body_id: Mapped[int] = mapped_column(ForeignKey("body.id"))
    engine_id: Mapped[int] = mapped_column(ForeignKey("engine.id"))

    body: Mapped["Body"] = relationship(back_populates="cars")
    engine: Mapped["Engine"] = relationship(back_populates="cars")
    maintenances: Mapped[List["Maintenance"]] = relationship(
        back_populates="car"
    )
    owner: Mapped["User"] = relationship(back_populates="cars")

    def __repr__(self):
        return f"Car: {self.brand}-{self.model}. Owner: {self.owner}"
