from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend

from tgbot.config import load_config
from tgbot.db.models import (
    User, School,
    College, Texnikum, Lyceum
)
from tgbot.misc.database import db


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        request.session.update({"token": config.db.secret_key})
        form = await request.form()

        await db.load()

        admin_login, admin_password = db.get_credentials()

        if form['username'] == admin_login and form['password'] == admin_password:
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        if not "token" in request.session:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


app = FastAPI()
config = load_config(".env")
engine = db.get_engine()
authentication_backend = AdminAuth(secret_key=config.db.secret_key)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)


class UserAdmin(ModelView, model=User):
    column_list = [User.user_id, User.username, User.first_name]
    can_create = False
    can_edit = False
    can_delete = False
    icon = "fa-solid fa-user"
    name_plural = "Foydalanuvchilar"

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class SchoolAdmin(ModelView, model=School):
    column_list = [
        School.malumot, School.rahbariyat,
        School.yonalish, School.qabul, School.savollar, School.boglanish
    ]
    icon = "fa-solid fa-university"
    name_plural = "Kasb-hunar maktabi"

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class CollegeAdmin(ModelView, model=College):
    column_list = [
        College.malumot, College.rahbariyat,
        College.yonalish, College.qabul, College.savollar, College.boglanish
    ]
    icon = "fa-solid fa-university"
    name_plural = "Kollej"

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class TexnikumAdmin(ModelView, model=Texnikum):
    column_list = [
        Texnikum.malumot, Texnikum.rahbariyat,
        Texnikum.yonalish, Texnikum.qabul, Texnikum.savollar, Texnikum.boglanish
    ]
    icon = "fa-solid fa-university"
    name_plural = "Texnikum"

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class LyceumAdmin(ModelView, model=Lyceum):
    column_list = [
        Lyceum.malumot, Lyceum.rahbariyat,
        Lyceum.yonalish, Lyceum.qabul, Lyceum.savollar, Lyceum.boglanish
    ]
    icon = "fa-solid fa-university"
    name_plural = "Litsey"

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


admin.add_view(UserAdmin)
admin.add_view(SchoolAdmin)
admin.add_view(CollegeAdmin)
admin.add_view(TexnikumAdmin)
admin.add_view(LyceumAdmin)
