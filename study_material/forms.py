from django import forms
from .models import StudyMaterial


class StudyMaterialForm(forms.ModelForm):

    class Meta:
        model = StudyMaterial

        fields = [
            "section",
            "subject",
            "title",
            "description",
            "material_type",
            "file",
            "is_active",
        ]

        widgets = {

            "section": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "subject": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder":
                        "Enter material title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder":
                        "Enter description"
                }
            ),

            "material_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }