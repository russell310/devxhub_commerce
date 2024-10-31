from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from .managers import AdminManager, CustomerManager


# Create your models here.

class CustomUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')


class Admin(CustomUser):
    objects = AdminManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        admin_group, created = Group.objects.get_or_create(name="admin")
        self.groups.add(admin_group)


class Customer(CustomUser):
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        customer_group, created = Group.objects.get_or_create(name="customer")
        self.groups.add(customer_group)
