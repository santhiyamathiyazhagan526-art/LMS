from django import forms

from .models import Assignment


class AssignmentForm(forms.ModelForm):

    class Meta:

        model = Assignment

        fields = [
            "title",
            "description",
            "subject",
            "section",
            "google_classroom_link",
            "is_active",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter assignment title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter description (optional)",
                }
            ),

            "subject": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "section": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "google_classroom_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Paste Google Classroom link",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }