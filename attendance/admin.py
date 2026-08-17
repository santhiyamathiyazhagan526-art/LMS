from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "attendance_date",
        "student",
        "subject",
        "staff",
        "status",
    )

    list_filter = (
        "attendance_date",
        "subject",
        "status",
    )

    search_fields = (
        "student__register_no",
        "student__name",
    )