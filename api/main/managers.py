from django.contrib.auth.models import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, id, username=None, fullname=None, user_lang='uz', password=None):
        if not id:
            raise ValueError('The User ID must be set.')

        user = self.model(
            id=id,
            username=username,
            fullname=fullname,
            user_lang=user_lang
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, username=None, fullname=None, user_lang='uz', password=None):
        user = self.create_user(
            id=id,
            username=username,
            fullname=fullname,
            user_lang=user_lang,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
