from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime
    car_id: Optional[int]
    driver_license_id: Optional[int]
    insurance_id: Optional[int]
    document_id: Optional[int]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    car_id: Optional[int]
    driver_license_id: Optional[int]
    insurance_id: Optional[int]
    document_id: Optional[int]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
