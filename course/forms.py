from django import forms
from .models import Course


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course

        fields = [
            "department",
            "name",
            "code",
            "duration",
            "total_semesters",
            "description",
            "is_active",
        ]

        widgets = {
            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Course Name"
            }),

            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Course Code"
            }),

            "duration": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Duration (Years)"
            }),

            "total_semesters": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Total Semesters"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Description"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }