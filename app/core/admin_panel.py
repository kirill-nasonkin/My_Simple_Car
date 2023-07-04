from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy.ext.asyncio import AsyncEngine

from app.models.cars import Car
from app.models.users import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.username,
    ]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id, User.username, User.email]
    icon = "fa-solid fa-user"


class CarAdmin(ModelView, model=Car):
    column_list = "__all__"
    column_searchable_list = [Car.model]
    icon = "fa-solid fa-car-side"


def setup_admin(app: FastAPI, engine: AsyncEngine):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(CarAdmin)
