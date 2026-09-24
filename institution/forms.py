from django import forms
from .models import Institution


class InstitutionForm(forms.ModelForm):

    class Meta:
        model = Institution

        fields = [
            "name",
            "code",
            "email",
            "phone",
            "website",
            "address",
            "city",
            "state",
            "country",
            "pincode",
            "logo",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter institution name",
            }),

            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter institution code",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email address",
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number",
            }),

            "website": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://example.com",
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter complete address",
                "rows": 3,
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter city",
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter state",
            }),

            "country": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter country",
            }),

            "pincode": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter pincode",
            }),

            "logo": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }