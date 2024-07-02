from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model
from .models import Agency
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
    add_fieldsets = (
        (None, {'fields':  ('first_name', 'last_name', 'email', 'phone', 'is_staff','is_active','is_partner', 'image',"password1", "password2",)}),
    )
    fieldsets = (
        (None, {
            "fields": (
                ('first_name', 'last_name', 'email', 'phone', 'is_staff','is_active','is_partner', 'image')
                
            ),
        }),
    )
admin.site.register(User,UserAdmin)


class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name','user','rating']
    list_per_page = 10
    search_fields = ['description']
admin.site.register(Agency, AgencyAdmin)
    