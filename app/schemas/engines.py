from enum import Enum

from pydantic import BaseModel, ConfigDict


class FuelTypeName(str, Enum):
    diesel = "diesel"
    gasoline = "gasoline"


class EngineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    model: str
    fuel_type: FuelTypeName
    volume: float
    power: int
    # cars: list = []


class EngineCreate(BaseModel):
    model: str
    fuel_type: FuelTypeName
    volume: float
    power: int = 100


class EngineUpdate(BaseModel):
    model: str | None
    fuel_type: FuelTypeName | None
    volume: float | None
    power: int | None
