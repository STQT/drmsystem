from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Organization

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {"fields": ("id", "password")}),
    #     ("Important dates", {"fields": ("last_login",)}),
    # )
    list_display = ["id", "username", "fullname", "stopped"]
    list_display_links = ['id', 'fullname']
    search_fields = ["id", "username"]

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
