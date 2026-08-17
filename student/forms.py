from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            "photo",
            "register_no",
            "name",
            "email",
            "gender",
            "institution",
            "department",
            "course",
            "section",
            "programme",
            "year",
            "is_active",
        ]

        widgets = {

            "register_no": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Register Number"
            }),

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Student Name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Email"
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

            "course": forms.Select(attrs={
                "class": "form-select"
            }),

            "section": forms.Select(attrs={
                "class": "form-select"
            }),

            "programme": forms.Select(attrs={
                "class": "form-select"
            }),
                        

            "year": forms.Select(attrs={
                "class": "form-select"
            }),

            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }