from django.db import models
from institution.models import Institution
from department.models import Department
from course.models import Course


class Section(models.Model):

    PROGRAMME_CHOICES = [
        ("UG", "UG"),
        ("PG", "PG"),
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

    programme = models.CharField(
        max_length=2,
        choices=PROGRAMME_CHOICES,
        default="UG"
    )

    YEAR_CHOICES = [
    ("I", "I Year"),
    ("II", "II Year"),
    ("III", "III Year"),
    ("IV", "IV Year"),

    ("PG-I", "PG I Year"),
    ("PG-II", "PG II Year"),
]

    year = models.CharField(
        max_length=10,
        choices=YEAR_CHOICES
    )

    section = models.CharField(
        max_length=10
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["programme", "course", "year", "section"]
        unique_together = (
            "course",
            "programme",
            "year",
            "section"
        )

    def __str__(self):
        return f"{self.programme} - {self.course} - {self.year} - {self.section}"