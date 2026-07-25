from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "subject_code",
        "subject_name",
        "department",
        "course",
        "semester",
        "credits",
        "staff",
        "is_active",
    )

    search_fields = (
        "subject_code",
        "subject_name",
    )

    list_filter = (
        "department",
        "course",
        "semester",
        "is_active",
    )