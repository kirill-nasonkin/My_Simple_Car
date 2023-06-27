import redis.asyncio
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    RedisStrategy,
)

from app.auth.manager import get_user_manager
from app.core.config import settings
from app.models.users import User

cookie_transport = CookieTransport(
    cookie_name="my-simple-car-auth",
    cookie_max_age=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
)

redis = redis.asyncio.from_url("redis://localhost:6379", decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(
        redis, lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )


auth_backend = AuthenticationBackend(
    name="cookie_redis",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user()
