from django.contrib import admin

from .models import (
    OnlineExam,
    OnlineExamSubmission
)


# ==========================================
# ONLINE EXAM ADMIN
# ==========================================

@admin.register(OnlineExam)
class OnlineExamAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "subject",
        "section",
        "exam_date",
        "start_time",
        "end_time",
        "total_marks",
        "is_active",
        "created_by",
    )

    list_filter = (
        "is_active",
        "exam_date",
        "subject",
        "section",
    )

    search_fields = (
        "title",
        "exam_link",
    )


# ==========================================
# SUBMISSION ADMIN
# ==========================================

@admin.register(OnlineExamSubmission)
class OnlineExamSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        "exam",
        "student",
        "submitted_at",
        "marks",
        "status",
    )

    list_filter = (
        "status",
        "submitted_at",
    )

    search_fields = (
        "exam__title",
        "student__name",
        "student__register_no",
    )