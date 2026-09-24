from django.db import models

from accounts.models import User
from section.models import Section
from subject.models import Subject
from student.models import Student


# ==========================================
# ONLINE EXAM
# ==========================================

class OnlineExam(models.Model):

    title = models.CharField(
        max_length=200
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )

    exam_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    total_marks = models.PositiveIntegerField(
        default=100
    )

    exam_link = models.URLField(
        max_length=500
    )

    instructions = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="online_exams_created"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-exam_date",
            "-start_time"
        ]

    def __str__(self):
        return self.title


# ==========================================
# ONLINE EXAM SUBMISSION
# ==========================================

class OnlineExamSubmission(models.Model):

    STATUS_CHOICES = [
        ("Submitted", "Submitted"),
        ("Evaluated", "Evaluated"),
    ]

    exam = models.ForeignKey(
        OnlineExam,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="online_exam_submissions"
    )

    answer_file = models.FileField(
        upload_to="online_exam_answers/"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    marks = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Submitted"
    )

    class Meta:
        ordering = [
            "-submitted_at"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "exam",
                    "student"
                ],
                name="unique_online_exam_submission"
            )
        ]

    def __str__(self):
        return (
            f"{self.exam.title} - "
            f"{self.student.name}"
        )