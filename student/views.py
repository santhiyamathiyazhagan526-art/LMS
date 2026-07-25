from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Student
from .forms import StudentForm
from department.models import Department
from course.models import Course


@login_required(login_url="login")
def student_list(request):

    search = request.GET.get("search", "").strip()
    department = request.GET.get("department", "")
    course = request.GET.get("course", "")

    students = Student.objects.select_related(
        "institution",
        "department",
        "course"
    ).order_by("name")

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(register_no__icontains=search) |
            Q(email__icontains=search)
        )

    if department:
        students = students.filter(department_id=department)

    if course:
        students = students.filter(course_id=course)

    total_students = Student.objects.count()
    active_students = Student.objects.filter(is_active=True).count()
    inactive_students = Student.objects.filter(is_active=False).count()

    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

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

    return render(request, "student/student_list.html", context)


@login_required(login_url="login")
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request, "Student added successfully.")

            return redirect("student_list")

    else:

        form = StudentForm()

    context = {
        "form": form,
        "title": "Add Student",
        "button": "Save Student",
    }

    return render(request, "student/student_form.html", context)


@login_required(login_url="login")
def edit_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Student updated successfully.")

            return redirect("student_list")

    else:

        form = StudentForm(instance=student)

    context = {
        "form": form,
        "title": "Edit Student",
        "button": "Update Student",
    }

    return render(request, "student/student_form.html", context)


@login_required(login_url="login")
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    student.delete()

    messages.success(request, "Student deleted successfully.")

    return redirect("student_list")