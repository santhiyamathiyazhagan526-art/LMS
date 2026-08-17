from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from staff.models import Staff
from section.models import Section
from subject.models import Subject

from .models import StudyMaterial
from .forms import StudyMaterialForm


# ==========================================================
# STAFF - STUDY MATERIAL LIST
# ==========================================================

@login_required(login_url="login")
def study_material_list(request):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    materials = StudyMaterial.objects.filter(
        staff=staff
    ).select_related(
        "section",
        "section__course",
        "subject"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "study_material/study_material_list.html",
        {
            "staff": staff,
            "materials": materials,
        }
    )


# ==========================================================
# STAFF - ADD STUDY MATERIAL
# ==========================================================

@login_required(login_url="login")
def add_study_material(request):

    # ------------------------------------------------------
    # Logged-in staff
    # ------------------------------------------------------

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    # ------------------------------------------------------
    # Staff subjects
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
    # Sections related to staff subjects
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

        form = StudyMaterialForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            material = form.save(
                commit=False
            )

            # ------------------------------------------------
            # Logged-in staff
            # ------------------------------------------------

            material.staff = staff

            # ------------------------------------------------
            # Selected section
            # ------------------------------------------------

            section = material.section

            if not section:

                messages.error(
                    request,
                    "Please select a section."
                )

                return render(
                    request,
                    "study_material/study_material_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Study Material",
                        "button": "Upload Material",
                    }
                )

            # ------------------------------------------------
            # Selected subject
            # ------------------------------------------------

            subject = material.subject

            if not subject:

                messages.error(
                    request,
                    "Please select a subject."
                )

                return render(
                    request,
                    "study_material/study_material_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Study Material",
                        "button": "Upload Material",
                    }
                )

            # ------------------------------------------------
            # Subject must belong to logged-in staff
            # ------------------------------------------------

            if subject.staff_id != staff.id:

                messages.error(
                    request,
                    "You can upload material only for your subjects."
                )

                return render(
                    request,
                    "study_material/study_material_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Study Material",
                        "button": "Upload Material",
                    }
                )

            # ------------------------------------------------
            # Section and Subject must belong
            # to the same Course
            # ------------------------------------------------

            if section.course_id != subject.course_id:

                messages.error(
                    request,
                    "Selected section does not belong to the selected subject course."
                )

                return render(
                    request,
                    "study_material/study_material_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Add Study Material",
                        "button": "Upload Material",
                    }
                )

            # ------------------------------------------------
            # SAVE
            # ------------------------------------------------

            material.save()

            messages.success(
                request,
                "Study material uploaded successfully."
            )

            return redirect(
                "study_material_list"
            )

        else:

            print("======================================")
            print("STUDY MATERIAL FORM ERRORS")
            print(form.errors)
            print("======================================")

    else:

        # ==================================================
        # GET
        # ==================================================

        form = StudyMaterialForm()

    # ======================================================
    # ALWAYS RETURN PAGE
    # ======================================================

    return render(
        request,
        "study_material/study_material_form.html",
        {
            "staff": staff,
            "form": form,
            "sections": sections,
            "subjects": subjects,
            "title": "Add Study Material",
            "button": "Upload Material",
        }
    )


# ==========================================================
# STAFF - EDIT STUDY MATERIAL
# ==========================================================

@login_required(login_url="login")
def edit_study_material(request, id):

    # ------------------------------------------------------
    # Logged-in staff
    # ------------------------------------------------------

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    # ------------------------------------------------------
    # Get material belonging to this staff
    # ------------------------------------------------------

    material = get_object_or_404(
        StudyMaterial,
        id=id,
        staff=staff
    )

    # ------------------------------------------------------
    # Staff subjects
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
    # Sections related to staff subjects
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

        form = StudyMaterialForm(
            request.POST,
            request.FILES,
            instance=material
        )

        if form.is_valid():

            updated_material = form.save(
                commit=False
            )

            # ------------------------------------------------
            # Keep logged-in staff
            # ------------------------------------------------

            updated_material.staff = staff

            # ------------------------------------------------
            # Selected section
            # ------------------------------------------------

            section = updated_material.section

            if not section:

                messages.error(
                    request,
                    "Please select a section."
                )

                return render(
                    request,
                    "study_material/study_material_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "material": material,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Edit Study Material",
                        "button": "Update Material",
                    }
                )

            # ------------------------------------------------
            # Selected subject
            # ------------------------------------------------

            subject = updated_material.subject

            if not subject:

                messages.error(
                    request,
                    "Please select a subject."
                )

                return render(
                    request,
                    "study_material/study_material_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "material": material,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Edit Study Material",
                        "button": "Update Material",
                    }
                )

            # ------------------------------------------------
            # Subject must belong to logged-in staff
            # ------------------------------------------------

            if subject.staff_id != staff.id:

                messages.error(
                    request,
                    "You can use only your assigned subjects."
                )

                return render(
                    request,
                    "study_material/study_material_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "material": material,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Edit Study Material",
                        "button": "Update Material",
                    }
                )

            # ------------------------------------------------
            # Section and Subject must belong
            # to same Course
            # ------------------------------------------------

            if section.course_id != subject.course_id:

                messages.error(
                    request,
                    "Selected section does not belong to the selected subject course."
                )

                return render(
                    request,
                    "study_material/study_material_form.html",
                    {
                        "staff": staff,
                        "form": form,
                        "material": material,
                        "sections": sections,
                        "subjects": subjects,
                        "title": "Edit Study Material",
                        "button": "Update Material",
                    }
                )

            # ------------------------------------------------
            # SAVE UPDATE
            # ------------------------------------------------

            updated_material.save()

            messages.success(
                request,
                "Study material updated successfully."
            )

            return redirect(
                "study_material_list"
            )

        else:

            print("======================================")
            print("EDIT STUDY MATERIAL FORM ERRORS")
            print(form.errors)
            print("======================================")

    else:

        # ==================================================
        # GET
        # ==================================================

        form = StudyMaterialForm(
            instance=material
        )

    # ======================================================
    # Existing Programme / Year / Section
    # ======================================================

    current_programme = ""
    current_year = ""
    current_section_id = ""

    if material.section:

        current_section = material.section

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

    # ======================================================
    # RETURN EDIT PAGE
    # ======================================================

    return render(
        request,
        "study_material/study_material_form.html",
        {
            "staff": staff,
            "form": form,
            "material": material,
            "sections": sections,
            "subjects": subjects,

            "title": "Edit Study Material",
            "button": "Update Material",

            "current_programme":
                current_programme,

            "current_year":
                current_year,

            "current_section_id":
                current_section_id,
        }
    )


# ==========================================================
# STAFF - DELETE STUDY MATERIAL
# ==========================================================

@login_required(login_url="login")
def delete_study_material(request, id):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )

    material = get_object_or_404(
        StudyMaterial,
        id=id,
        staff=staff
    )

    material.delete()

    messages.success(
        request,
        "Study material deleted successfully."
    )

    return redirect(
        "study_material_list"
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

    # ------------------------------------------------------
    # UG
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # PG
    # ------------------------------------------------------

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

    print("======================================")
    print("STUDY MATERIAL - GET SECTIONS")
    print("Staff:", staff.staff_id)
    print("Programme:", programme)
    print("Year:", year)
    print("======================================")

    # ------------------------------------------------------
    # Courses assigned to this staff through subjects
    # ------------------------------------------------------

    subject_courses = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).values_list(
        "course_id",
        flat=True
    )

    # ------------------------------------------------------
    # Find matching sections
    #
    # UG:
    # I / II / III / IV
    #
    # PG:
    # PG-I / PG-II
    #
    # Do NOT convert PG-II to II.
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

        print(
            "FOUND SECTION:",
            section.id,
            "| Course:",
            section.course.name,
            "| Programme:",
            section.course.programme,
            "| Year:",
            section.year,
            "| Section:",
            section.section
        )

        data.append({
            "id": section.id,
            "name": section.section,
        })

    print(
        "RETURNING:",
        data
    )

    return JsonResponse(
        data,
        safe=False
    )