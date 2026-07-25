from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)

    email = models.EmailField()
    phone = models.CharField(max_length=15)

    website = models.URLField(blank=True)

    address = models.TextField()

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    logo = models.ImageField(
        upload_to="institution_logos/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name