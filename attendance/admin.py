from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "attendance_date",
        "student",
        "subject",
        "status",
        "staff",
    )

    list_filter = (
        "attendance_date",
        "subject",
        "status",
    )

    search_fields = (
        "student__student_name",
        "subject__subject_name",
    )