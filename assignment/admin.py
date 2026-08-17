from django.contrib import admin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "subject",
        "section",
        "staff",
        "google_classroom_link",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "subject",
        "section",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "google_classroom_link",
        "subject__subject_name",
        "staff__staff_id",
    )

    ordering = (
        "-created_at",
    )