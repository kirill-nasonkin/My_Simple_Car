from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    registered_at: datetime | None
    is_active: bool | None = True
    is_superuser: bool = False


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str | None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None


class UserRead(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
