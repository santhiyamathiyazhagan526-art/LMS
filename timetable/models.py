from django.db import models

from section.models import Section
from subject.models import Subject
from staff.models import Staff


class Timetable(models.Model):

    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    PERIOD_CHOICES = [
        ("1", "Period 1"),
        ("2", "Period 2"),
        ("3", "Period 3"),
        ("4", "Period 4"),
        ("5", "Period 5"),
        ("6", "Period 6"),
    ]

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="timetables"
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="timetables"
    )

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="timetables"
    )

    day = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    period = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES
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
            "day",
            "period"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "section",
                    "day",
                    "period"
                ],
                name="unique_section_day_period"
            )
        ]

    def __str__(self):
        return (
            f"{self.section} - "
            f"{self.day} - "
            f"{self.period} - "
            f"{self.subject}"
        )