from django.db import models
from institution.models import Institution
from department.models import Department


class Course(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    name = models.CharField(max_length=150)

    code = models.CharField(
        max_length=20,
        unique=True
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in Years"
    )

    total_semesters = models.PositiveIntegerField()

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name