from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Timetable
from .forms import TimetableForm

from staff.models import Staff


# ==========================================================
# TIMETABLE LIST
# ==========================================================

@login_required(login_url="login")
def timetable_list(request):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    timetables = Timetable.objects.filter(
        is_active=True
    ).select_related(
        "section",
        "section__course",
        "subject",
        "staff"
    ).order_by(
        "section__course__programme",
        "section__year",
        "section__section",
        "day",
        "period"
    )

    return render(
        request,
        "timetable/timetable_list.html",
        {
            "staff": staff,
            "timetables": timetables,
        }
    )


# ==========================================================
# ADD TIMETABLE
# ==========================================================

@login_required(login_url="login")
def add_timetable(request):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    if request.method == "POST":

        form = TimetableForm(
            request.POST
        )

        if form.is_valid():

            timetable = form.save(
                commit=False
            )

            # ------------------------------------------------
            # Check duplicate timetable slot
            # ------------------------------------------------

            existing = Timetable.objects.filter(
                section=timetable.section,
                day=timetable.day,
                period=timetable.period,
                is_active=True
            ).exists()

            if existing:

                messages.error(
                    request,
                    "This section already has a timetable for the selected day and period."
                )

            else:

                timetable.save()

                messages.success(
                    request,
                    "Timetable added successfully."
                )

                return redirect(
                    "staff_timetable"
                )

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = TimetableForm()

    return render(
        request,
        "timetable/timetable_form.html",
        {
            "staff": staff,
            "form": form,
            "title": "Add Timetable",
            "button_text": "Save Timetable",
        }
    )


# ==========================================================
# EDIT TIMETABLE
# ==========================================================

@login_required(login_url="login")
def edit_timetable(request, id):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    timetable = get_object_or_404(
        Timetable,
        id=id
    )

    if request.method == "POST":

        form = TimetableForm(
            request.POST,
            instance=timetable
        )

        if form.is_valid():

            updated_timetable = form.save(
                commit=False
            )

            existing = Timetable.objects.filter(
                section=updated_timetable.section,
                day=updated_timetable.day,
                period=updated_timetable.period,
                is_active=True
            ).exclude(
                id=timetable.id
            ).exists()

            if existing:

                messages.error(
                    request,
                    "Another timetable already exists for this section, day and period."
                )

            else:

                updated_timetable.save()

                messages.success(
                    request,
                    "Timetable updated successfully."
                )

                return redirect(
                    "staff_timetable"
                )

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = TimetableForm(
            instance=timetable
        )

    return render(
        request,
        "timetable/timetable_form.html",
        {
            "staff": staff,
            "form": form,
            "title": "Edit Timetable",
            "button_text": "Update Timetable",
            "timetable": timetable,
        }
    )


# ==========================================================
# DELETE TIMETABLE
# ==========================================================

@login_required(login_url="login")
def delete_timetable(request, id):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    timetable = get_object_or_404(
        Timetable,
        id=id
    )

    timetable.delete()

    messages.success(
        request,
        "Timetable deleted successfully."
    )

    return redirect(
        "staff_timetable"
    )