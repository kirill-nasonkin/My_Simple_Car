from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.settings import settings
from app.core.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from app.db.session import get_async_session

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login.
    Provide an access token for future requests.
    Set HTTPOnly Cookie.
    """
    user = await crud.user.authenticate(
        session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.UserRead)
async def test_token(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
async def recover_password(
    email: str,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Password Recovery
    """
    user = await crud.user.get_by_email(session, email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
    user = await crud.user.get_by_email(session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    hashed_password = security.get_password_hash(new_password)
    user.hashed_password = hashed_password
    session.add(user)
    await session.commit()
    return {"msg": "Password updated successfully"}


@router.post("/logout")
async def logout(
    response: Response,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Logout
    """
    response.set_cookie(
        key="access_token", value=f"", max_age=0, httponly=True
    )
