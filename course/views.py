from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Course
from .forms import CourseForm
from institution.models import Institution
from department.models import Department


@login_required(login_url="login")
def course_list(request):

    search = request.GET.get("search", "").strip()
    department = request.GET.get("department", "")

    courses = Course.objects.select_related(
        "institution",
        "department"
    ).order_by("name")
    
    if search:
        courses = courses.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(department__name__icontains=search)
        )

    if department:
        courses = courses.filter(department_id=department)

    total_courses = Course.objects.count()
    active_courses = Course.objects.filter(is_active=True).count()
    inactive_courses = Course.objects.filter(is_active=False).count()

    paginator = Paginator(courses, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
    "courses": page_obj,
    "page_obj": page_obj,
    "search": search,
    "selected_department": department,
    "departments": Department.objects.all(),
    "total_courses": total_courses,
    "active_courses": active_courses,
    "inactive_courses": inactive_courses,
}

    return render(request, "course/course_list.html", context)


@login_required(login_url="login")
def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            course = form.save(commit=False)

            institution = Institution.objects.first()

            if institution:
                course.institution = institution

            course.save()

            messages.success(request, "Course added successfully.")

            return redirect("course_list")

    else:

        form = CourseForm()

    context = {
        "form": form,
        "title": "Add Course",
        "button": "Save Course",
    }

    return render(request, "course/course_form.html", context)


@login_required(login_url="login")
def edit_course(request, id):

    course = get_object_or_404(Course, id=id)

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            course = form.save(commit=False)

            institution = Institution.objects.first()

            if institution:
                course.institution = institution

            course.save()

            messages.success(request, "Course updated successfully.")

            return redirect("course_list")

    else:

        form = CourseForm(instance=course)

    context = {
        "form": form,
        "title": "Edit Course",
        "button": "Update Course",
    }

    return render(request, "course/course_form.html", context)


@login_required(login_url="login")
def delete_course(request, id):

    course = get_object_or_404(Course, id=id)

    course.delete()

    messages.success(request, "Course deleted successfully.")

    return redirect("course_list")