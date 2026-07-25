from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        fields = [
            "institution",
            "department",
            "course",
            "subject_code",
            "subject_name",
            "semester",
            "credits",
            "staff",
            "is_active",
        ]

        widgets = {

            "institution": forms.Select(attrs={
                "class": "form-select"
            }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            "course": forms.Select(attrs={
                "class": "form-select"
            }),

            "subject_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Subject Code"
            }),

            "subject_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Subject Name"
            }),

            "semester": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 8
            }),

            "credits": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 10
            }),

            "staff": forms.Select(attrs={
                "class": "form-select"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }