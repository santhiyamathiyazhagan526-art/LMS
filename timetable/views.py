from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Timetable
from .forms import TimetableForm
from staff.models import Staff


@login_required(login_url="login")
def timetable_list(request):

    # Logged-in staff
    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    # IMPORTANT:
    # Only show this staff member's timetable.
    timetables = (
        Timetable.objects
        .filter(
            staff=staff,
            is_active=True
        )
        .select_related(
            "section",
            "section__course",
            "subject"
        )
    )

    # Day Order
    # 1 = Monday
    # 2 = Tuesday
    # 3 = Wednesday
    # 4 = Thursday
    # 5 = Friday
    # 6 = Saturday

    day_orders = [
        ("Monday", 1),
        ("Tuesday", 2),
        ("Wednesday", 3),
        ("Thursday", 4),
        ("Friday", 5),
        ("Saturday", 6),
    ]

    # IMPORTANT:
    # Get period values directly from the model.
    # Timetable.period is a CharField.
    periods = Timetable.PERIOD_CHOICES

    timetable_rows = []

    for period_value, period_label in periods:

        row = {
            "value": period_value,
            "label": period_label,
            "cells": []
        }

        for day_name, day_order in day_orders:

            entry = timetables.filter(
                day=day_name,
                period=period_value
            ).first()

            row["cells"].append({
                "day_name": day_name,
                "day_order": day_order,
                "entry": entry,
            })

        timetable_rows.append(row)

    context = {
        "staff": staff,
        "day_orders": day_orders,
        "timetable_rows": timetable_rows,
    }

    return render(
        request,
        "timetable/timetable_list.html",
        context
    )


@login_required(login_url="login")
def add_timetable(request):

    # Logged-in staff
    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    if request.method == "POST":

        form = TimetableForm(request.POST)

        if form.is_valid():

            timetable = form.save(commit=False)

            # IMPORTANT:
            # Automatically assign the logged-in staff.
            # The user cannot assign another staff member.
            timetable.staff = staff

            # Make sure period is stored as string.
            timetable.period = str(
                timetable.period
            )

            # Check duplicate section/day/period
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


@login_required(login_url="login")
def edit_timetable(request, id):

    # Logged-in staff
    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    # IMPORTANT:
    # Staff can edit ONLY their own timetable.
    timetable = get_object_or_404(
        Timetable,
        id=id,
        staff=staff
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

            # Keep the timetable assigned
            # to the logged-in staff.
            updated_timetable.staff = staff

            updated_timetable.period = str(
                updated_timetable.period
            )

            # Check duplicate
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


@login_required(login_url="login")
def delete_timetable(request, id):

    # Logged-in staff
    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    # Staff can delete ONLY their own timetable.
    timetable = get_object_or_404(
        Timetable,
        id=id,
        staff=staff
    )

    timetable.delete()

    messages.success(
        request,
        "Timetable deleted successfully."
    )

    return redirect(
        "staff_timetable"
    )