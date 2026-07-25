from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Department
from .forms import DepartmentForm
from institution.models import Institution


@login_required(login_url="login")
def department_list(request):
    search = request.GET.get("search", "")

    departments = Department.objects.select_related("institution").all()

    if search:
        departments = departments.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(dean_name__icontains=search) |
            Q(hod_name__icontains=search) |
            Q(email__icontains=search)
        )

    # Statistics
    total_departments = Department.objects.count()
    active_departments = Department.objects.filter(is_active=True).count()
    inactive_departments = Department.objects.filter(is_active=False).count()

    # Pagination
    paginator = Paginator(departments, 10)   # 10 records per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "departments": page_obj,
        "page_obj": page_obj,
        "search": search,
        "total_departments": total_departments,
        "active_departments": active_departments,
        "inactive_departments": inactive_departments,
    }

    return render(request, "department/department_list.html", context)


@login_required(login_url="login")
def add_department(request):

    if request.method == "POST":

        form = DepartmentForm(request.POST)

        if form.is_valid():

            department = form.save(commit=False)

            institution = Institution.objects.first()

            if institution:
                department.institution = institution

            department.save()

            messages.success(request, "Department added successfully.")

            return redirect("department_list")

    else:
        form = DepartmentForm()

    context = {
        "form": form,
        "title": "Add Department",
        "button": "Save Department",
    }

    return render(request, "department/department_form.html", context)


@login_required(login_url="login")
def edit_department(request, id):

    department = get_object_or_404(Department, id=id)

    if request.method == "POST":

        form = DepartmentForm(request.POST, instance=department)

        if form.is_valid():

            department = form.save(commit=False)

            institution = Institution.objects.first()

            if institution:
                department.institution = institution

            department.save()

            messages.success(request, "Department updated successfully.")

            return redirect("department_list")

    else:
        form = DepartmentForm(instance=department)

    context = {
        "form": form,
        "title": "Edit Department",
        "button": "Update Department",
    }

    return render(request, "department/department_form.html", context)