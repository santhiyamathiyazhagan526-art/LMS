from django.db import models
from student.models import Student
from subject.models import Subject
from staff.models import Staff
from section.models import Section


class Attendance(models.Model):

    STATUS_CHOICES = (
        ("Present", "Present"),
        ("Absent", "Absent"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )

    attendance_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Present"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "student",
            "subject",
            "attendance_date",
        )

        ordering = [
            "-attendance_date",
            "student__register_no"
        ]

    def __str__(self):
        return (
            f"{self.student.register_no} - "
            f"{self.subject.subject_name} - "
            f"{self.attendance_date}"
        )