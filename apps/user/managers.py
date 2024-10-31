from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class AdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name="admin")

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomerManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name="customer")

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
