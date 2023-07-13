from enum import Enum

from pydantic import BaseModel, ConfigDict, condecimal, field_validator


class FuelTypeName(str, Enum):
    diesel = "diesel"
    gasoline = "gasoline"


class EngineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    model: str
    fuel_type: FuelTypeName
    volume: str
    power: int


class EngineCreate(BaseModel):
    model: str
    fuel_type: FuelTypeName
    volume: condecimal(gt=0, decimal_places=1)
    power: int = 100

    @field_validator("model")
    def capitalize_model(cls, v: str):
        return v.upper()

    @field_validator("volume")
    def get_volume_string_value(cls, v: str):
        return str(float(v))


class EngineUpdate(EngineCreate):
    model: str | None
    fuel_type: FuelTypeName | None
    volume: condecimal(gt=0, decimal_places=1) | None
    power: int | None
