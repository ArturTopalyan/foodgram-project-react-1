from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


@admin.action(description='Забанить смертного')
def ban_user(modeladmin, request, queryset):
    queryset.update(is_blocked=True)


@admin.action(description='Помиловать смертного')
def unban_user(modeladmin, request, queryset):
    queryset.update(is_blocked=False)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'last_login',
        'is_active',
        'email',
    )
    list_editable = (
        'is_active',
    )
    list_filter = (
        'email',
        'username',
    )
    actions = (
        ban_user,
        unban_user,
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'author',
    )
