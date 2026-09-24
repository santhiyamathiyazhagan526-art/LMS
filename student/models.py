from django.db import models

from institution.models import Institution
from department.models import Department
from course.models import Course
from section.models import Section


class Student(models.Model):

    # ==========================================
    # GENDER
    # ==========================================

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]


    # ==========================================
    # PROGRAMME
    # ==========================================

    PROGRAMME_CHOICES = [
        ("UG", "Under Graduate"),
        ("PG", "Post Graduate"),
    ]


    # ==========================================
    # YEAR
    # ==========================================

    YEAR_CHOICES = [
        ("I", "I Year"),
        ("II", "II Year"),
        ("III", "III Year"),
        ("PG-I", "PG I Year"),
        ("PG-II", "PG II Year"),
    ]


    # ==========================================
    # LEARNING MODE
    # ==========================================

    LEARNING_MODE_CHOICES = [
        ("Online", "Online"),
        ("Offline", "Offline"),
    ]


    # ==========================================
    # STUDENT PHOTO
    # ==========================================

    photo = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )


    # ==========================================
    # REGISTER NUMBER
    # ==========================================

    register_no = models.CharField(
        max_length=30,
        unique=True
    )


    # ==========================================
    # NAME
    # ==========================================

    name = models.CharField(
        max_length=150
    )


    # ==========================================
    # EMAIL
    # ==========================================

    email = models.EmailField(
        unique=True
    )


    # ==========================================
    # GENDER
    # ==========================================

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )


    # ==========================================
    # INSTITUTION
    # ==========================================

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE
    )


    # ==========================================
    # DEPARTMENT
    # ==========================================

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )


    # ==========================================
    # COURSE
    # ==========================================

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )


    # ==========================================
    # SECTION
    # ==========================================

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    # ==========================================
    # PROGRAMME
    # ==========================================

    programme = models.CharField(
        max_length=2,
        choices=PROGRAMME_CHOICES,
        default="UG"
    )


    # ==========================================
    # YEAR
    # ==========================================

    year = models.CharField(
        max_length=5,
        choices=YEAR_CHOICES
    )


    # ==========================================
    # LEARNING MODE
    # ==========================================

    learning_mode = models.CharField(
        max_length=10,
        choices=LEARNING_MODE_CHOICES,
        default="Offline"
    )


    # ==========================================
    # ACTIVE STATUS
    # ==========================================

    is_active = models.BooleanField(
        default=True
    )


    # ==========================================
    # TIMESTAMPS
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    # ==========================================
    # META
    # ==========================================

    class Meta:
        ordering = ["name"]


    # ==========================================
    # STRING REPRESENTATION
    # ==========================================

    def __str__(self):
        return f"{self.register_no} - {self.name}"