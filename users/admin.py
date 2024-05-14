from django.contrib import admin
from users.models import User, Profile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # Add customizations to the UserAdmin class
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)