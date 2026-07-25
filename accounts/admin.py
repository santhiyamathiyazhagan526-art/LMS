from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'LMS Information',
            {
                'fields': (
                    'role',
                    'phone_number',
                    'profile_photo',
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )