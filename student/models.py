from django.db import models
from institution.models import Institution
from department.models import Department
from course.models import Course


class Student(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    YEAR_CHOICES = [
        ("I", "I Year"),
        ("II", "II Year"),
        ("III", "III Year"),
        ("IV", "IV Year"),
    ]

    photo = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )

    register_no = models.CharField(
        max_length=30,
        unique=True
    )

    name = models.CharField(
        max_length=150
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

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    year = models.CharField(
        max_length=5,
        choices=YEAR_CHOICES
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
        return f"{self.register_no} - {self.name}"