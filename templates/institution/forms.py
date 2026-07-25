from django import forms
from .models import Institution


class InstitutionForm(forms.ModelForm):

    class Meta:

        model = Institution

        fields = "__all__"

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "code": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "website": forms.URLInput(attrs={
                "class": "form-control"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "country": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "pincode": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }