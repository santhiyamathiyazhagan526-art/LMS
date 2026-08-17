from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from django.db import transaction

from .models import Staff
from .forms import StaffForm


@login_required
def staff_list(request):

    search = request.GET.get("search", "")

    staffs = Staff.objects.select_related(
        "institution",
        "department"
    ).all().order_by("name")

    if search:
        staffs = staffs.filter(
            Q(staff_id__icontains=search) |
            Q(name__icontains=search) |
            Q(email__icontains=search)
        )

    paginator = Paginator(staffs, 10)
    page = request.GET.get("page")
    staffs = paginator.get_page(page)

    context = {
        "staffs": staffs,
        "search": search,
        "total_staff": Staff.objects.count(),
        "active_staff": Staff.objects.filter(is_active=True).count(),
        "inactive_staff": Staff.objects.filter(is_active=False).count(),
    }

    return render(request, "staff/staff_list.html", context)


@login_required
def add_staff(request):

    if request.method == "POST":

        form = StaffForm(request.POST, request.FILES)

        if form.is_valid():

            try:
                with transaction.atomic():

                    # Save Staff
                    staff = form.save()

                    # Check if a login account already exists
                    if User.objects.filter(username=staff.staff_id).exists():
                        raise Exception("A login account with this Staff ID already exists.")

                    # Create Login Account
                    User.objects.create_user(
                        username=staff.staff_id,
                        email=staff.email,
                        password="Staff@123",
                        role="STAFF",
                        first_name=staff.name,
                        must_change_password=True,
                    )
                    messages.success(
                        request,
                        f"Staff added successfully.\n\n"
                        f"Username : {staff.staff_id}\n"
                        f"Password : Staff@123"
                    )

                    return redirect("staff_list")

            except Exception as e:

                messages.error(request, str(e))

    else:

        form = StaffForm()

    return render(
        request,
        "staff/staff_form.html",
        {
            "form": form,
            "title": "Add Staff",
            "button": "Save Staff",
        },
    )


@login_required
def edit_staff(request, pk):

    staff = get_object_or_404(Staff, pk=pk)

    if request.method == "POST":

        form = StaffForm(request.POST, request.FILES, instance=staff)

        if form.is_valid():
            form.save()
            messages.success(request, "Staff updated successfully.")
            return redirect("staff_list")

    else:
        form = StaffForm(instance=staff)

    return render(request, "staff/staff_form.html", {
        "form": form,
        "title": "Edit Staff",
        "button": "Update Staff",
    })


@login_required
def delete_staff(request, pk):

    staff = get_object_or_404(Staff, pk=pk)

    if request.method == "POST":
        staff.delete()
        messages.success(request, "Staff deleted successfully.")
        return redirect("staff_list")

    return render(request, "staff/confirm_delete.html", {
        "object": staff,
    })