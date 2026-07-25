from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q


from .forms import AttendanceFilterForm
from .models import Attendance

from student.models import Student
from institution.models import Institution
from department.models import Department
from course.models import Course
from subject.models import Subject
from staff.models import Staff
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# ==========================
# TAKE ATTENDANCE
# ==========================

@login_required
def take_attendance(request):

    form = AttendanceFilterForm()
    students = []

    if request.method == "POST":

        # Load Students
        if "load_students" in request.POST:

            form = AttendanceFilterForm(request.POST)

            if form.is_valid():

                institution = form.cleaned_data["institution"]
                department = form.cleaned_data["department"]
                course = form.cleaned_data["course"]

                students = Student.objects.filter(
                    institution=institution,
                    department=department,
                    course=course
                ).order_by("name")

        # Save Attendance
        elif "save_attendance" in request.POST:

            form = AttendanceFilterForm(request.POST)

            if form.is_valid():

                institution = form.cleaned_data["institution"]
                department = form.cleaned_data["department"]
                course = form.cleaned_data["course"]
                subject = form.cleaned_data["subject"]
                staff = form.cleaned_data["staff"]
                attendance_date = form.cleaned_data["attendance_date"]

                students = Student.objects.filter(
                    institution=institution,
                    department=department,
                    course=course
                ).order_by("name")

                for student in students:

                    status = request.POST.get(
                        f"status_{student.id}",
                        "Present"
                    )

                    Attendance.objects.update_or_create(
                        student=student,
                        subject=subject,
                        attendance_date=attendance_date,
                        defaults={
                            "institution": institution,
                            "department": department,
                            "course": course,
                            "staff": staff,
                            "status": status,
                        }
                    )

                messages.success(
                    request,
                    "Attendance saved successfully."
                )

                return redirect("attendance_history")

    return render(
        request,
        "attendance/attendance_form.html",
        {
            "form": form,
            "students": students,
        },
    )


# ==========================
# ATTENDANCE HISTORY
# ==========================

@login_required
def attendance_history(request):

    attendance = Attendance.objects.select_related(
        "institution",
        "department",
        "course",
        "subject",
        "staff",
        "student"
    )

    search = request.GET.get("search")
    institution = request.GET.get("institution")
    department = request.GET.get("department")
    course = request.GET.get("course")
    subject = request.GET.get("subject")
    staff = request.GET.get("staff")

    if search:
        attendance = attendance.filter(
            Q(student__name__icontains=search) |
            Q(student__register_no__icontains=search)
        )

    if institution:
        attendance = attendance.filter(institution_id=institution)

    if department:
        attendance = attendance.filter(department_id=department)

    if course:
        attendance = attendance.filter(course_id=course)

    if subject:
        attendance = attendance.filter(subject_id=subject)

    if staff:
        attendance = attendance.filter(staff_id=staff)

    attendance_records = (
        attendance.values(
            "subject_id",
            "attendance_date",
            "institution__name",
            "department__name",
            "course__name",
            "subject__subject_name",
            "staff__name",
        )
        .annotate(total_students=Count("student"))
        .order_by("-attendance_date")
    )

    context = {
        "attendance_records": attendance_records,
        "institutions": Institution.objects.all(),
        "departments": Department.objects.all(),
        "courses": Course.objects.all(),
        "subjects": Subject.objects.all(),
        "staffs": Staff.objects.all(),
    }

    return render(
        request,
        "attendance/attendance_history.html",
        context,
    )


# ==========================
# VIEW ATTENDANCE
# ==========================

@login_required
def view_attendance(request, subject_id, attendance_date):

    attendance_list = Attendance.objects.filter(
        subject_id=subject_id,
        attendance_date=attendance_date
    ).select_related(
        "student",
        "subject",
        "staff",
        "institution",
        "department",
        "course"
    ).order_by("student__name")

    attendance_info = attendance_list.first()

    return render(
        request,
        "attendance/view_attendance.html",
        {
            "attendance_list": attendance_list,
            "attendance_info": attendance_info,
        },
    )


# ==========================
# EDIT ATTENDANCE
# ==========================

@login_required
def edit_attendance(request, subject_id, attendance_date):

    attendance_list = Attendance.objects.filter(
        subject_id=subject_id,
        attendance_date=attendance_date
    ).select_related(
        "student",
        "subject",
        "staff",
        "institution",
        "department",
        "course"
    ).order_by("student__name")

    if not attendance_list.exists():
        messages.error(request, "Attendance record not found.")
        return redirect("attendance_history")

    if request.method == "POST":

        for attendance in attendance_list:

            status = request.POST.get(f"status_{attendance.id}")

            if status:
                attendance.status = status
                attendance.save()

        messages.success(
            request,
            "Attendance updated successfully."
        )

        return redirect("attendance_history")

    attendance_info = attendance_list.first()

    return render(
        request,
        "attendance/edit_attendance.html",
        {
            "attendance_list": attendance_list,
            "attendance_info": attendance_info,
        },
    )


# ==========================
# DELETE ATTENDANCE
# ==========================

@login_required
def delete_attendance(request, subject_id, attendance_date):

    attendance_list = Attendance.objects.filter(
        subject_id=subject_id,
        attendance_date=attendance_date
    ).select_related(
        "subject",
        "staff"
    )

    if not attendance_list.exists():
        messages.error(request, "Attendance record not found.")
        return redirect("attendance_history")

    attendance_info = attendance_list.first()

    if request.method == "POST":

        attendance_list.delete()

        messages.success(
            request,
            "Attendance deleted successfully."
        )

        return redirect("attendance_history")

    return render(
        request,
        "attendance/delete_attendance.html",
        {
            "attendance_info": attendance_info,
            "total_students": attendance_list.count(),
        },
    )
# ==========================
# EXPORT ATTENDANCE PDF
# ==========================

@login_required
def export_attendance_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="attendance_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))

    data = [[
        "Date",
        "Institution",
        "Department",
        "Course",
        "Subject",
        "Faculty",
        "Students"
    ]]

    attendance_records = (
        Attendance.objects.values(
            "attendance_date",
            "institution__name",
            "department__name",
            "course__name",
            "subject__subject_name",
            "staff__name",
        )
        .annotate(total_students=Count("student"))
        .order_by("-attendance_date")
    )

    for record in attendance_records:
        data.append([
            str(record["attendance_date"]),
            record["institution__name"],
            record["department__name"],
            record["course__name"],
            record["subject__subject_name"],
            record["staff__name"],
            record["total_students"],
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
    ]))

    doc.build([table])

    return response