from django.db import models
from institution.models import Institution
from department.models import Department


class Staff(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    photo = models.ImageField(
        upload_to="staff_photos/",
        blank=True,
        null=True
    )

    staff_id = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    designation = models.CharField(
        max_length=100
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

    def __str__(self):
        return f"{self.staff_id} - {self.name}"