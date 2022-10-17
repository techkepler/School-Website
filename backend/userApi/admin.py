from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

# admin.register(User)


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("uid", "role", "is_active")
    search_fields = (
        "uid",
        "role",
    )
    list_filter = ("uid", "role", "is_active", "is_staff")
    fieldsets = (
        ("User Credentials", {"fields": ("uid", "password")}),
        ("Personal info", {"fields": ("role",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_superuser",
                    "is_admin",
                    "is_staff",
                    "is_active",
                )
            },
        ),
        ("Other", {"fields": ("created_at", "updated_at")}),
        (
            "Group Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("uid", "role", "password1", "password2"),
            },
        ),
    )
    search_fields = ("uid",)
    ordering = ("uid", "id")
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
