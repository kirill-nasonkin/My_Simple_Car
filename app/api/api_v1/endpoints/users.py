from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.core.settings import settings
from app.db.session import get_async_session

router = APIRouter()


@router.get("/", response_model=list[schemas.UserRead])
async def read_users(
    session: AsyncSession = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Retrieve users."""
    users = await crud.user.get_multi(session, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.UserRead)
async def create_user(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Create new user. For superuser use only."""
    user = await crud.user.get_by_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create(session, create_schema=user_in)
    # todo check whether to leave
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email,
    #         username=user_in.email,
    #         password=user_in.password,
    #     )
    return user


@router.put("/me", response_model=schemas.UserRead)
async def update_user_me(
    *,
    session: AsyncSession = Depends(get_async_session),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """User self update."""
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = await crud.user.update(
        session, db_obj=current_user, update_schema=user_in
    )
    return user


@router.get("/me", response_model=schemas.UserRead)
async def read_user_me(
    session: AsyncSession = Depends(get_async_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get current user."""
    return current_user


@router.post("/open", response_model=schemas.UserRead)
async def create_user_open(
    *,
    session: AsyncSession = Depends(get_async_session),
    email: EmailStr = Body(...),
    password: str = Body(..., min_length=settings.PASSWORD_MIN_LENGTH),
    full_name: str = Body(None),
) -> Any:
    """
    Registration for basic users.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server",
        )
    user = await crud.user.get_by_email(session, email=email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(
        password=password, email=email, full_name=full_name
    )
    user = await crud.user.create(session, create_schema=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.UserRead)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """Get specific user by the ID."""
    user = await crud.user.get(session, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.put("/{user_id}", response_model=schemas.UserRead)
async def update_user(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Update specific user with the ID provided."""
    user = await crud.user.get(session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update(session, db_obj=user, update_schema=user_in)
    return user
