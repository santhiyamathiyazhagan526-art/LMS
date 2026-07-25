from django.db import models
from institution.models import Institution
from department.models import Department
from course.models import Course
from staff.models import Staff


class Subject(models.Model):

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

    subject_code = models.CharField(
        max_length=20,
        unique=True
    )

    subject_name = models.CharField(
        max_length=200
    )

    semester = models.PositiveIntegerField()

    credits = models.PositiveIntegerField()

    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"