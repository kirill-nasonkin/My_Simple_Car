from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy.ext.asyncio import AsyncEngine

from app.models import (
    Body,
    Car,
    Document,
    DriverLicense,
    Engine,
    Image,
    Insurance,
    Maintenance,
    User,
)


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.username,
    ]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = column_list
    icon = "fa-solid fa-user"


class DriverLicenseAdmin(ModelView, model=DriverLicense):
    column_list = "__all__"
    column_searchable_list = [DriverLicense.user]
    column_sortable_list = [
        DriverLicense.id,
        DriverLicense.start_date,
        DriverLicense.exp_date,
        DriverLicense.user,
    ]
    icon = "fa-solid fa-id-card"


class InsuranceAdmin(ModelView, model=Insurance):
    column_list = "__all__"
    column_searchable_list = [Insurance.user, Insurance.insurer]
    column_sortable_list = [
        Insurance.id,
        Insurance.insurer,
        Insurance.start_date,
        Insurance.exp_date,
        Insurance.user,
    ]
    icon = "fa-solid fa-file-invoice"


class DocumentAdmin(ModelView, model=Document):
    column_list = "__all__"
    column_searchable_list = [Document.user, Document.title]
    column_sortable_list = [
        Document.id,
        Document.title,
        Document.start_date,
        Document.exp_date,
        Document.user,
    ]
    icon = "fa-sharp fa-solid fa-file-contract"


class CarAdmin(ModelView, model=Car):
    column_list = [Car.id, Car.model, Car.brand, Car.year_built]
    column_searchable_list = [Car.model, Car.owner]
    column_sortable_list = column_list
    icon = "fa-solid fa-car-side"


class ImageAdmin(ModelView, model=Image):
    column_list = [Image.id, Image.title]
    column_searchable_list = [Image.title, Image.car, Image.body]
    column_sortable_list = column_list
    icon = "fa-solid fa-images"


class BodyAdmin(ModelView, model=Body):
    column_list = [Body.id, Body.title]
    column_searchable_list = [Body.title]
    column_sortable_list = column_list
    icon = "fa-solid fa-car"


class EngineAdmin(ModelView, model=Engine):
    column_list = [
        Engine.id,
        Engine.model,
        Engine.fuel_type,
        Engine.volume,
        Engine.power,
    ]
    column_searchable_list = [Engine.model]
    column_sortable_list = column_list
    icon = "fa-solid fa-gear"


class MaintenanceAdmin(ModelView, model=Maintenance):
    column_list = [
        Maintenance.id,
        Maintenance.title,
        Maintenance.date,
        Maintenance.car,
    ]
    column_searchable_list = [Maintenance.title, Maintenance.car]
    column_sortable_list = column_list
    icon = "fa-solid fa-wrench"


def setup_admin(app: FastAPI, engine: AsyncEngine):
    admin_views = (
        BodyAdmin,
        CarAdmin,
        DocumentAdmin,
        DriverLicenseAdmin,
        EngineAdmin,
        ImageAdmin,
        InsuranceAdmin,
        MaintenanceAdmin,
        UserAdmin,
    )
    admin = Admin(app, engine)
    for view in admin_views:
        admin.add_view(view)
