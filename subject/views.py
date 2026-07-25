from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Subject
from .forms import SubjectForm
from department.models import Department
from course.models import Course


@login_required
def subject_list(request):

    search = request.GET.get("search", "")
    department = request.GET.get("department", "")
    course = request.GET.get("course", "")

    subjects = Subject.objects.select_related(
        "institution",
        "department",
        "course",
        "staff"
    ).all()

    if search:
        subjects = subjects.filter(
            Q(subject_name__icontains=search) |
            Q(subject_code__icontains=search)
        )

    if department:
        subjects = subjects.filter(department_id=department)

    if course:
        subjects = subjects.filter(course_id=course)

    paginator = Paginator(subjects, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "subjects": page_obj,
        "page_obj": page_obj,

        "departments": Department.objects.all(),
        "courses": Course.objects.all(),

        "search": search,
        "selected_department": department,
        "selected_course": course,

        "total_subjects": Subject.objects.count(),
        "active_subjects": Subject.objects.filter(is_active=True).count(),
        "inactive_subjects": Subject.objects.filter(is_active=False).count(),
    }

    return render(request, "subject/subject_list.html", context)


@login_required
def add_subject(request):

    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Subject added successfully.")
            return redirect("subject_list")
    else:
        form = SubjectForm()

    return render(request, "subject/subject_form.html", {
        "form": form,
        "title": "Add Subject"
    })

@login_required
def edit_subject(request, pk):

    subject = get_object_or_404(Subject, pk=pk)

    if request.method == "POST":

        form = SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect("subject_list")

    else:
        form = SubjectForm(instance=subject)

    return render(request, "subject/subject_form.html", {
        "form": form,
        "title": "Edit Subject"
    })


@login_required
def delete_subject(request, pk):

    subject = get_object_or_404(Subject, pk=pk)

    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
        return redirect("subject_list")

    return render(request, "subject/confirm_delete.html", {
        "object": subject
    })