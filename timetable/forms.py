from django import forms

from .models import Timetable
from section.models import Section
from subject.models import Subject


class TimetableForm(forms.ModelForm):

    class Meta:

        model = Timetable

        fields = [
            "section",
            "subject",
            "day",
            "period",
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

            "day": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "period": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        # ---------------------------------------------
        # SECTIONS
        # ---------------------------------------------

        self.fields["section"].queryset = (
            Section.objects
            .filter(
                is_active=True
            )
            .select_related(
                "course"
            )
            .order_by(
                "programme",
                "course__name",
                "year",
                "section"
            )
        )

        # ---------------------------------------------
        # SUBJECTS
        # ---------------------------------------------

        self.fields["subject"].queryset = (
            Subject.objects
            .filter(
                is_active=True
            )
            .select_related(
                "course"
            )
            .order_by(
                "course__programme",
                "subject_name"
            )
        )