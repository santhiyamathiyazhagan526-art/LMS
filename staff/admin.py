from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = (
        "staff_id",
        "name",
        "email",
        "gender",
        "institution",
        "department",
        "designation",
        "is_active",
    )

    search_fields = (
        "staff_id",
        "name",
        "email",
    )

    list_filter = (
        "institution",
        "department",
        "designation",
        "is_active",
    )