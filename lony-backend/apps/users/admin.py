from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Informations supplémentaires", {'fields': ('phone', 'avatar', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informations supplémentaires", {'fields': ('phone', 'avatar', 'role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
