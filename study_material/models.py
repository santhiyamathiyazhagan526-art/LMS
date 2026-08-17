from django.db import models

from staff.models import Staff
from subject.models import Subject
from section.models import Section


class StudyMaterial(models.Model):

    MATERIAL_TYPE_CHOICES = [
        ("PDF", "PDF"),
        ("PPT", "PowerPoint"),
        ("DOC", "Document"),
        ("VIDEO", "Video"),
        ("OTHER", "Other"),
    ]

    # Staff who uploaded the material
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="study_materials"
    )

    # Subject
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="study_materials"
    )

    # Section
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="study_materials"
    )

    # Material title
    title = models.CharField(
        max_length=200
    )

    # Description
    description = models.TextField(
        blank=True,
        null=True
    )

    # Uploaded file
    file = models.FileField(
        upload_to="study_materials/"
    )

    # Material type
    material_type = models.CharField(
        max_length=10,
        choices=MATERIAL_TYPE_CHOICES,
        default="PDF"
    )

    # Active / inactive
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
            "-created_at"
        ]

    def __str__(self):
        return self.title