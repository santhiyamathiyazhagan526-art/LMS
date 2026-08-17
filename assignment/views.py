from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from staff.models import Staff
from subject.models import Subject
from section.models import Section

from .models import Assignment
from .forms import AssignmentForm


# ==========================================================
# STAFF - ASSIGNMENT LIST
# ==========================================================

@login_required(login_url="login")
def assignment_list(request):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    assignments = Assignment.objects.filter(
        staff=staff
    ).select_related(
        "subject",
        "section",
        "section__course"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "assignment/staff_assignments.html",
        {
            "staff": staff,
            "assignments": assignments,
        }
    )


# ==========================================================
# STAFF - ADD ASSIGNMENT
# ==========================================================

@login_required(login_url="login")
def add_assignment(request):

    # ------------------------------------------------------
    # Logged-in staff
    # ------------------------------------------------------

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    # ------------------------------------------------------
    # Subjects assigned to this staff
    # ------------------------------------------------------

    subjects = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "subject_name"
    )

    # ------------------------------------------------------
    # Courses handled by this staff
    # ------------------------------------------------------

    subject_courses = subjects.values_list(
        "course_id",
        flat=True
    )

    # ------------------------------------------------------
    # Sections belonging to staff subjects
    # ------------------------------------------------------

    sections = Section.objects.filter(
        course_id__in=subject_courses,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "course__programme",
        "year",
        "section"
    )

    # ------------------------------------------------------
    # POST - SAVE ASSIGNMENT
    # ------------------------------------------------------

    if request.method == "POST":

        form = AssignmentForm(
            request.POST
        )

        if form.is_valid():

            assignment = form.save(
                commit=False
            )

            # Logged-in staff
            assignment.staff = staff

            section = assignment.section
            subject = assignment.subject

            # --------------------------------------------------
            # Section validation
            # --------------------------------------------------

            if not section:

                messages.error(
                    request,
                    "Please select a section."
                )

                return render(
                    request,
                    "assignment/assignment_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Assignment",
                        "button": "Save Assignment",
                    }
                )

            # --------------------------------------------------
            # Subject validation
            # --------------------------------------------------

            if not subject:

                messages.error(
                    request,
                    "Please select a subject."
                )

                return render(
                    request,
                    "assignment/assignment_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Assignment",
                        "button": "Save Assignment",
                    }
                )

            # --------------------------------------------------
            # Subject must belong to logged-in staff
            # --------------------------------------------------

            if subject.staff_id != staff.id:

                messages.error(
                    request,
                    "You can create assignments only for your subjects."
                )

                return render(
                    request,
                    "assignment/assignment_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Assignment",
                        "button": "Save Assignment",
                    }
                )

            # --------------------------------------------------
            # Section and subject must belong to same course
            # --------------------------------------------------

            if section.course_id != subject.course_id:

                messages.error(
                    request,
                    "Selected section does not belong to the selected subject course."
                )

                return render(
                    request,
                    "assignment/assignment_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Assignment",
                        "button": "Save Assignment",
                    }
                )

            # --------------------------------------------------
            # SAVE
            # --------------------------------------------------

            assignment.save()

            messages.success(
                request,
                "Assignment link saved successfully."
            )

            return redirect(
                "staff_assignments"
            )

        else:

            # Show validation errors in terminal
            print("================================")
            print("ASSIGNMENT FORM ERRORS")
            print(form.errors)
            print("================================")

    else:

        # --------------------------------------------------
        # GET - EMPTY FORM
        # --------------------------------------------------

        form = AssignmentForm()

    # ------------------------------------------------------
    # IMPORTANT:
    # Render FORM, not assignment list
    # ------------------------------------------------------

    return render(
        request,
        "assignment/assignment_form.html",
        {
            "staff": staff,
            "form": form,
            "sections": sections,
            "subjects": subjects,
            "title": "Add Assignment",
            "button": "Save Assignment",
        }
    )

    # ------------------------------------------------------
    # Subjects assigned to this staff
    # ------------------------------------------------------

    subjects = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "subject_name"
    )

    # ------------------------------------------------------
    # Courses handled by staff
    # ------------------------------------------------------

    subject_courses = subjects.values_list(
        "course_id",
        flat=True
    )

    # ------------------------------------------------------
    # Sections belonging to those courses
    # ------------------------------------------------------

    sections = Section.objects.filter(
        course_id__in=subject_courses,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "course__programme",
        "year",
        "section"
    )

    # ======================================================
    # POST
    # ======================================================

    if request.method == "POST":

        form = AssignmentForm(
            request.POST
        )

        if form.is_valid():

            assignment = form.save(
                commit=False
            )

            assignment.staff = staff

            section = assignment.section
            subject = assignment.subject

            # ------------------------------------------------
            # Section required
            # ------------------------------------------------

            if not section:

                messages.error(
                    request,
                    "Please select a section."
                )

                return render(
                    request,
                    "assignment/staff_assignments.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Assignment",
                        "button": "Save Assignment",
                    }
                )

            # ------------------------------------------------
            # Subject required
            # ------------------------------------------------

            if not subject:

                messages.error(
                    request,
                    "Please select a subject."
                )

                return render(
                    request,
                    "assignment/staff_assignments.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Assignment",
                        "button": "Save Assignment",
                    }
                )

            # ------------------------------------------------
            # Subject must belong to logged-in staff
            # ------------------------------------------------

            if subject.staff_id != staff.id:

                messages.error(
                    request,
                    "You can create assignments only for your subjects."
                )

                return render(
                    request,
                    "assignment/staff_assignments.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Assignment",
                        "button": "Save Assignment",
                    }
                )

            # ------------------------------------------------
            # Section and Subject must belong
            # to same course
            # ------------------------------------------------

            if section.course_id != subject.course_id:

                messages.error(
                    request,
                    "Selected section does not belong to the selected subject course."
                )

                return render(
                    request,
                    "assignment/staff_assignments.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Assignment",
                        "button": "Save Assignment",
                    }
                )

            # ------------------------------------------------
            # Save
            # ------------------------------------------------

            assignment.save()

            messages.success(
                request,
                "Assignment link saved successfully."
            )

            return redirect(
                "staff_assignments"
            )

        else:

            print("================================")
            print("ASSIGNMENT FORM ERRORS")
            print(form.errors)
            print("================================")

    else:

        form = AssignmentForm()

    return render(
        request,
        "assignment/staff_assignments.html",
        {
            "staff": staff,
            "form": form,
            "sections": sections,
            "subjects": subjects,
            "title": "Add Assignment",
            "button": "Save Assignment",
        }
    )


# ==========================================================
# STAFF - EDIT ASSIGNMENT
# ==========================================================

@login_required(login_url="login")
def edit_assignment(request, id):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    assignment = get_object_or_404(
        Assignment,
        id=id,
        staff=staff
    )

    subjects = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "subject_name"
    )

    subject_courses = subjects.values_list(
        "course_id",
        flat=True
    )

    sections = Section.objects.filter(
        course_id__in=subject_courses,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "course__programme",
        "year",
        "section"
    )

    # ======================================================
    # POST
    # ======================================================

    if request.method == "POST":

        form = AssignmentForm(
            request.POST,
            instance=assignment
        )

        if form.is_valid():

            updated_assignment = form.save(
                commit=False
            )

            updated_assignment.staff = staff

            section = updated_assignment.section
            subject = updated_assignment.subject

            if not section:

                messages.error(
                    request,
                    "Please select a section."
                )

                return render(
                    request,
                    "assignment/staff_assignments.html",
                    {
                        "staff": staff,
                        "form": form,
                        "assignment": assignment,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Edit Assignment",
                        "button": "Update Assignment",
                    }
                )

            if not subject:

                messages.error(
                    request,
                    "Please select a subject."
                )

                return render(
                    request,
                    "assignment/assignment_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "assignment": assignment,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Edit Assignment",
                        "button": "Update Assignment",
                    }
                )

            if subject.staff_id != staff.id:

                messages.error(
                    request,
                    "You can use only your assigned subjects."
                )

                return render(
                    request,
                    "assignment/assignment_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "assignment": assignment,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Edit Assignment",
                        "button": "Update Assignment",
                    }
                )

            if section.course_id != subject.course_id:

                messages.error(
                    request,
                    "Selected section does not belong to the selected subject course."
                )

                return render(
                    request,
                    "assignment/assignment_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "assignment": assignment,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Edit Assignment",
                        "button": "Update Assignment",
                    }
                )

            updated_assignment.save()

            messages.success(
                request,
                "Assignment updated successfully."
            )

            return redirect(
                "staff_assignments"
            )

        else:

            print("================================")
            print("EDIT ASSIGNMENT FORM ERRORS")
            print(form.errors)
            print("================================")

    else:

        form = AssignmentForm(
            instance=assignment
        )

    # ------------------------------------------------------
    # Existing programme/year/section
    # ------------------------------------------------------

    current_programme = ""
    current_year = ""
    current_section_id = ""

    if assignment.section:

        current_section = assignment.section

        if current_section.course:

            current_programme = (
                current_section.course.programme
            )

        current_year = (
            current_section.year
        )

        current_section_id = (
            current_section.id
        )

    return render(
        request,
        "assignment/assignment_form.html",
        {
            "staff": staff,
            "form": form,
            "assignment": assignment,
            "sections": sections,
            "subjects": subjects,

            "title": "Edit Assignment",
            "button": "Update Assignment",

            "current_programme":
                current_programme,

            "current_year":
                current_year,

            "current_section_id":
                current_section_id,
        }
    )


# ==========================================================
# STAFF - DELETE ASSIGNMENT
# ==========================================================

@login_required(login_url="login")
def delete_assignment(request, id):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    assignment = get_object_or_404(
        Assignment,
        id=id,
        staff=staff
    )

    assignment.delete()

    messages.success(
        request,
        "Assignment deleted successfully."
    )

    return redirect(
        "staff_assignments"
    )


# ==========================================================
# AJAX - GET YEARS
# ==========================================================

@login_required(login_url="login")
def get_years(request):

    programme = request.GET.get(
        "programme",
        ""
    ).strip()

    if programme == "UG":

        data = [
            {
                "value": "I",
                "text": "I Year"
            },
            {
                "value": "II",
                "text": "II Year"
            },
            {
                "value": "III",
                "text": "III Year"
            },
            {
                "value": "IV",
                "text": "IV Year"
            },
        ]

    elif programme == "PG":

        data = [
            {
                "value": "PG-I",
                "text": "PG I Year"
            },
            {
                "value": "PG-II",
                "text": "PG II Year"
            },
        ]

    else:

        data = []

    return JsonResponse(
        data,
        safe=False
    )


# ==========================================================
# AJAX - GET SECTIONS
# ==========================================================

@login_required(login_url="login")
def get_sections(request):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    programme = request.GET.get(
        "programme",
        ""
    ).strip()

    year = request.GET.get(
        "year",
        ""
    ).strip()

    # ------------------------------------------------------
    # Courses assigned through staff subjects
    # ------------------------------------------------------

    subject_courses = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).values_list(
        "course_id",
        flat=True
    )

    # ------------------------------------------------------
    # Find sections
    #
    # PG-II remains PG-II.
    # No conversion to II.
    # ------------------------------------------------------

    sections = Section.objects.filter(
        course_id__in=subject_courses,
        course__programme=programme,
        year=year,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "section"
    )

    data = []

    for section in sections:

        data.append({
            "id": section.id,
            "name": section.section,
        })

    return JsonResponse(
        data,
        safe=False
    )