from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'student_id', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'student_id')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Datos académicos', {'fields': ('student_id',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Datos personales', {'fields': ('email', 'student_id',)}),
    )

