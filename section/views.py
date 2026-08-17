from multiprocessing import context
from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Section
from institution.models import Institution
from department.models import Department
from course.models import Course


def section_list(request):

    sections = Section.objects.select_related(
        "institution",
        "department",
        "course"
    )

    total_sections = sections.count()

    active_sections = sections.filter(
        is_active=True
    ).count()

    inactive_sections = sections.filter(
        is_active=False
    ).count()

    context = {
        "sections": sections,
        "total_sections": total_sections,
        "active_sections": active_sections,
        "inactive_sections": inactive_sections,
    }

    return render(request, "section/section_list.html", context)

def add_section(request):

    if request.method == "POST":

        institution = Institution.objects.get(
            id=request.POST["institution"]
        )

        department = Department.objects.get(
            id=request.POST["department"]
        )

        course = Course.objects.get(
            id=request.POST["course"]
        )

        Section.objects.create(

            institution=institution,
            department=department,
            course=course,

            year=request.POST["year"],
            section=request.POST["section"],

            is_active="is_active" in request.POST

        )

        messages.success(request, "Section Added Successfully")

        return redirect("section_list")

    context = {

        "institutions": Institution.objects.all(),
        "departments": Department.objects.all(),
        "courses": Course.objects.all(),
    }
    print("Courses Count:", context["courses"].count())
    print("Courses:", list(context["courses"].values()))

    return render(request, "section/add_section.html", context)


# Edit Section
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Section
from institution.models import Institution
from department.models import Department
from course.models import Course


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Section
from institution.models import Institution
from department.models import Department
from course.models import Course


def edit_section(request, pk):

    # Get existing section
    section = get_object_or_404(
        Section.objects.select_related(
            "institution",
            "department",
            "course"
        ),
        pk=pk
    )

    # Dropdown data
    institutions = Institution.objects.all().order_by("name")

    departments = Department.objects.all().order_by("name")

    # Get all active courses
    # JavaScript will filter UG / PG courses
    courses = Course.objects.filter(
        is_active=True
    ).select_related(
        "department"
    ).order_by("name")


    # ==================================================
    # POST
    # ==================================================

    if request.method == "POST":

        institution_id = request.POST.get("institution")
        department_id = request.POST.get("department")
        programme = request.POST.get("programme")
        course_id = request.POST.get("course")
        year = request.POST.get("year")
        section_name = request.POST.get("section", "").strip()

        is_active = (
            request.POST.get("is_active") == "on"
        )


        # ----------------------------------------------
        # Validate Institution
        # ----------------------------------------------

        institution = get_object_or_404(
            Institution,
            pk=institution_id
        )


        # ----------------------------------------------
        # Validate Department
        # ----------------------------------------------

        department = get_object_or_404(
            Department,
            pk=department_id
        )


        # ----------------------------------------------
        # Validate Course
        # ----------------------------------------------

        course = get_object_or_404(
            Course,
            pk=course_id
        )


        # ----------------------------------------------
        # Validate Programme
        # ----------------------------------------------

        if programme not in ["UG", "PG"]:

            messages.error(
                request,
                "Please select a valid programme."
            )

            return redirect(
                "edit_section",
                pk=section.pk
            )


        # ----------------------------------------------
        # Course must match Programme
        # ----------------------------------------------

        if course.programme != programme:

            messages.error(
                request,
                "Selected course does not belong to the selected programme."
            )

            return redirect(
                "edit_section",
                pk=section.pk
            )


        # ----------------------------------------------
        # Course must belong to Department
        # ----------------------------------------------

        if course.department_id != department.id:

            messages.error(
                request,
                "Selected course does not belong to the selected department."
            )

            return redirect(
                "edit_section",
                pk=section.pk
            )


        # ----------------------------------------------
        # Validate Year
        # ----------------------------------------------

        if programme == "UG":

            valid_years = [
                "I",
                "II",
                "III",
                "IV",
            ]

        else:

            valid_years = [
                "PG-I",
                "PG-II",
            ]


        if year not in valid_years:

            messages.error(
                request,
                "Please select a valid year."
            )

            return redirect(
                "edit_section",
                pk=section.pk
            )


        # ----------------------------------------------
        # Section validation
        # ----------------------------------------------

        if not section_name:

            messages.error(
                request,
                "Section name is required."
            )

            return redirect(
                "edit_section",
                pk=section.pk
            )


        # ----------------------------------------------
        # Update Section
        # ----------------------------------------------

        section.institution = institution

        section.department = department

        section.course = course

        section.year = year

        section.section = section_name

        section.is_active = is_active

        section.save()


        messages.success(
            request,
            "Section updated successfully."
        )

        return redirect("section_list")


    # ==================================================
    # GET
    # ==================================================

    current_programme = section.course.programme


    context = {
        "section": section,

        "institutions": institutions,

        "departments": departments,

        "courses": courses,

        # Programme comes from Course
        "programme": current_programme,
    }


    return render(
        request,
        "section/edit_section.html",
        context
    )
# Delete Section
def delete_section(request, pk):

    section = get_object_or_404(Section, pk=pk)

    section.delete()

    messages.success(request, "Section Deleted Successfully")

    return redirect("section_list")