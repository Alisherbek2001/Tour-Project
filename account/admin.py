from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(DjangoUserAdmin):
    ordering = ("pk",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_active",
        "is_partner"
    )
admin.site.register(User,UserAdmin)