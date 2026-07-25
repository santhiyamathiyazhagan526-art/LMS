from django.contrib import admin
from .models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "email",
        "phone",
        "city",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "email",
    )

    list_filter = (
        "city",
        "state",
        "is_active",
    )