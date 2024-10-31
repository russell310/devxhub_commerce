from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import Admin, Customer

# Register your models here.

admin.site.unregister(EmailAddress)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


@admin.register(Admin)
class AdminAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'created_at', 'updated_at']
    fieldsets = None


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'created_at', 'updated_at']
    fieldsets = None