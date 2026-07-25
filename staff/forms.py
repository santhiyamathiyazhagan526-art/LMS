from django import forms
from .models import Staff


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = [
            "photo",
            "staff_id",
            "name",
            "email",
            "gender",
            "institution",
            "department",
            "designation",
            "is_active",
        ]

        widgets = {

            "photo": forms.FileInput(attrs={
                "class": "form-control"
            }),

            "staff_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Staff ID"
            }),

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Staff Name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Email Address"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "institution": forms.Select(attrs={
                "class": "form-select"
            }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            "designation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Designation"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }