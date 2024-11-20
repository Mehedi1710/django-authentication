from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add fields to display in the list view
    list_display = ['username', 'email', 'first_name', 'last_name', 'birthdate']
    # Add fields to the form view
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birthdate', 'profile_picture')}),
    )
    # Add fields for creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('birthdate', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
