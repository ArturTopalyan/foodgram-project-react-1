from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'last_login',
        'is_active',
        'password',
        'email',
    )
    list_editable = (
        'password',
        'is_active',
    )
    list_filter = (
        'email',
        'username',
    )
