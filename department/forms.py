from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'name',
            'code',
            'dean_name',
            'hod_name',
            'email',
            'phone',
            'description',
            'is_active'
        ]

        widgets = {
            'institution': forms.Select(attrs={
                'class': 'form-select'
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Department Name'
            }),

            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Department Code'
            }),
            'dean_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Dean Name'
            }),

            'hod_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter HOD Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Department Description'
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }