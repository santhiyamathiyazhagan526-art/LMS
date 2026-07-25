from django.db import models
from institution.models import Institution


class Department(models.Model):

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    dean_name = models.CharField(
    max_length=100
    )
    hod_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    description = models.TextField(
        blank=True,
        null=True
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
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name