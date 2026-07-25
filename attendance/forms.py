from django import forms
from .models import Attendance
from institution.models import Institution
from department.models import Department
from course.models import Course
from subject.models import Subject
from staff.models import Staff


class AttendanceFilterForm(forms.Form):

    institution = forms.ModelChoiceField(
        queryset=Institution.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    staff = forms.ModelChoiceField(
        queryset=Staff.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    attendance_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )