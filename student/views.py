from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Student
from .forms import StudentForm

from department.models import Department
from course.models import Course
from section.models import Section


User = get_user_model()


# =========================================================
# CLASSES
# =========================================================

@login_required(login_url="login")
def classes(request):

    sections = Section.objects.filter(
        is_active=True
    ).select_related(
        "institution",
        "department",
        "course"
    ).order_by(
        "programme",
        "year",
        "section"
    )

    # -----------------------------------------------------
    # UG
    # -----------------------------------------------------

    ug_sections = sections.filter(
        programme="UG"
    )

    ug_years = []

    for year_code, year_name in Section.YEAR_CHOICES:

        if year_code not in ["I", "II", "III"]:
            continue

        year_sections = ug_sections.filter(
            year=year_code
        )

        if year_sections.exists():

            ug_years.append({
                "code": year_code,
                "name": year_name,
                "sections": year_sections,
            })


    # -----------------------------------------------------
    # PG
    # -----------------------------------------------------

    pg_sections = sections.filter(
        programme="PG"
    )

    pg_years = []

    for year_code, year_name in Section.YEAR_CHOICES:

        if year_code not in ["PG-I", "PG-II"]:
            continue

        year_sections = pg_sections.filter(
            year=year_code
        )

        if year_sections.exists():

            pg_years.append({
                "code": year_code,
                "name": year_name,
                "sections": year_sections,
            })


    context = {
        "ug_years": ug_years,
        "pg_years": pg_years,
    }

    return render(
        request,
        "student/classes.html",
        context
    )


# =========================================================
# STUDENTS OF A PARTICULAR CLASS
# =========================================================

@login_required(login_url="login")
def class_students(request, section_id):

    section = get_object_or_404(
        Section.objects.select_related(
            "institution",
            "department",
            "course"
        ),
        id=section_id,
        is_active=True
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    students = Student.objects.filter(
        section=section
    ).select_related(
        "institution",
        "department",
        "course",
        "section"
    ).order_by("name")


    if search:

        students = students.filter(
            Q(name__icontains=search) |
            Q(register_no__icontains=search) |
            Q(email__icontains=search)
        )


    total_students = Student.objects.filter(
        section=section
    ).count()

    active_students = Student.objects.filter(
        section=section,
        is_active=True
    ).count()

    inactive_students = Student.objects.filter(
        section=section,
        is_active=False
    ).count()


    paginator = Paginator(
        students,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )


    context = {
        "section": section,
        "students": page_obj,
        "page_obj": page_obj,
        "search": search,
        "total_students": total_students,
        "active_students": active_students,
        "inactive_students": inactive_students,
    }


    return render(
        request,
        "student/class_students.html",
        context
    )


# =========================================================
# ADD STUDENT TO CLASS
# =========================================================

@login_required(login_url="login")
@transaction.atomic
def add_student_to_class(
    request,
    section_id
):

    section = get_object_or_404(
        Section.objects.select_related(
            "institution",
            "department",
            "course"
        ),
        id=section_id,
        is_active=True
    )


    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            student = form.save(
                commit=False
            )

            # Force selected class information
            student.section = section
            student.institution = section.institution
            student.department = section.department
            student.course = section.course
            student.programme = section.programme
            student.year = section.year

            student.save()


            # -------------------------------------------------
            # Create login account
            # -------------------------------------------------

            existing_user = User.objects.filter(
                username=student.register_no
            ).first()


            if existing_user is None:

                User.objects.create_user(
                    username=student.register_no,
                    password=student.register_no,
                    email=student.email,
                    first_name=student.name,
                    role="STUDENT",
                    must_change_password=True
                )

                messages.success(
                    request,
                    "Student added successfully. Student login account created."
                )

            else:

                messages.success(
                    request,
                    "Student added successfully to this class."
                )


            return redirect(
                "class_students",
                section_id=section.id
            )


    else:

        form = StudentForm(
            initial={
                "institution": section.institution,
                "department": section.department,
                "course": section.course,
                "programme": section.programme,
                "year": section.year,
                "section": section,
            }
        )


    context = {
        "form": form,
        "title": "Add Student",
        "button": "Save Student",
        "section": section,
        "class_mode": True,
    }


    return render(
        request,
        "student/student_form.html",
        context
    )


# =========================================================
# STUDENT LIST
# =========================================================

@login_required(login_url="login")
def student_list(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    department = request.GET.get(
        "department",
        ""
    )

    course = request.GET.get(
        "course",
        ""
    )


    students = Student.objects.select_related(
        "institution",
        "department",
        "course",
        "section"
    ).order_by("name")


    if search:

        students = students.filter(
            Q(name__icontains=search) |
            Q(register_no__icontains=search) |
            Q(email__icontains=search)
        )


    if department:

        students = students.filter(
            department_id=department
        )


    if course:

        students = students.filter(
            course_id=course
        )


    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        is_active=True
    ).count()

    inactive_students = Student.objects.filter(
        is_active=False
    ).count()


    paginator = Paginator(
        students,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )


    context = {
        "students": page_obj,
        "page_obj": page_obj,
        "search": search,
        "selected_department": department,
        "selected_course": course,
        "departments": Department.objects.all().order_by("name"),
        "courses": Course.objects.all().order_by("name"),
        "total_students": total_students,
        "active_students": active_students,
        "inactive_students": inactive_students,
    }


    return render(
        request,
        "student/student_list.html",
        context
    )


# =========================================================
# ADD STUDENT
# =========================================================

@login_required(login_url="login")
@transaction.atomic
def add_student(request):

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            student = form.save()


            existing_user = User.objects.filter(
                username=student.register_no
            ).first()


            if existing_user is None:

                User.objects.create_user(
                    username=student.register_no,
                    password=student.register_no,
                    email=student.email,
                    first_name=student.name,
                    role="STUDENT",
                    must_change_password=True
                )

                messages.success(
                    request,
                    "Student added successfully. Student login account created."
                )

            else:

                messages.success(
                    request,
                    "Student added successfully. A login account already exists for this register number."
                )


            return redirect(
                "student_list"
            )


    else:

        form = StudentForm()


    context = {
        "form": form,
        "title": "Add Student",
        "button": "Save Student",
    }


    return render(
        request,
        "student/student_form.html",
        context
    )


# =========================================================
# EDIT STUDENT
# =========================================================

@login_required(login_url="login")
@transaction.atomic
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    old_register_no = student.register_no


    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )


        if form.is_valid():

            updated_student = form.save()


            user = User.objects.filter(
                username=old_register_no,
                role="STUDENT"
            ).first()


            if user is None:

                username_exists = User.objects.filter(
                    username=updated_student.register_no
                ).exists()


                if username_exists:

                    messages.error(
                        request,
                        "This register number is already used by another login account."
                    )

                    return redirect(
                        "edit_student",
                        id=id
                    )


                User.objects.create_user(
                    username=updated_student.register_no,
                    password=updated_student.register_no,
                    email=updated_student.email,
                    first_name=updated_student.name,
                    role="STUDENT",
                    must_change_password=True
                )


            else:

                if old_register_no != updated_student.register_no:

                    username_exists = User.objects.filter(
                        username=updated_student.register_no
                    ).exclude(
                        id=user.id
                    ).exists()


                    if username_exists:

                        messages.error(
                            request,
                            "This register number is already used by another login account."
                        )

                        return redirect(
                            "edit_student",
                            id=id
                        )


                    user.username = updated_student.register_no


                user.email = updated_student.email
                user.first_name = updated_student.name

                user.save()


            messages.success(
                request,
                "Student updated successfully."
            )


            return redirect(
                "student_list"
            )


    else:

        form = StudentForm(
            instance=student
        )


    context = {
        "form": form,
        "title": "Edit Student",
        "button": "Update Student",
    }


    return render(
        request,
        "student/student_form.html",
        context
    )


# =========================================================
# DELETE STUDENT
# =========================================================

@login_required(login_url="login")
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    student.delete()


    messages.success(
        request,
        "Student deleted successfully."
    )


    return redirect(
        "student_list"
    )