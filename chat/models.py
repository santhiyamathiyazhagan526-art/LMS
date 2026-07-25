from django.db import models
from institution.models import Institution
from department.models import Department
from course.models import Course
from subject.models import Subject
from staff.models import Staff
from student.models import Student


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    ]

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
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

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    attendance_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Present'
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-attendance_date', 'student']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.attendance_date}"