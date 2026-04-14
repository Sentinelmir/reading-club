from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Reading_Club.accounts.models import BaseUser


@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'nickname', 'is_staff')
    search_fields = ('username', 'email', 'nickname')