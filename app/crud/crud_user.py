from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import User
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    async def get_by_email(
        session: AsyncSession, *, email: str
    ) -> User | None:
        statement = select(User).where(User.email == email)
        results = await session.execute(statement)
        return results.scalar_one_or_none()

    async def create(
        self, session: AsyncSession, *, create_schema: UserCreate
    ) -> User:
        db_obj = User(
            email=create_schema.email,
            full_name=create_schema.full_name,
            hashed_password=get_password_hash(create_schema.password),
            is_superuser=create_schema.is_superuser,
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: User,
        update_schema: UserUpdate | dict[str, Any]
    ) -> User:
        if isinstance(update_schema, dict):
            update_data = update_schema
        else:
            update_data = update_schema.model_dump(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(
            session, db_obj=db_obj, update_schema=update_data
        )

    async def authenticate(
        self, session: AsyncSession, *, email: str, password: str
    ) -> User | None:
        user: User = await self.get_by_email(session, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    @staticmethod
    def is_superuser(user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
