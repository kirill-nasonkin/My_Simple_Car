from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy.ext.asyncio import AsyncEngine

from app.models.users import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]


def setup_admin(app: FastAPI, engine: AsyncEngine):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
