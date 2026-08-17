from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q

from student.models import Student
from subject.models import Subject
from study_material.models import StudyMaterial
from assignment.models import Assignment
from timetable.models import Timetable
from attendance.models import Attendance


@login_required(login_url="login")
def student_dashboard(request):

    # Only students can access Student Portal
    if request.user.role != "STUDENT":
        return redirect("login")

    # Get Student record using login username
    student = get_object_or_404(
        Student,
        register_no=request.user.username,
        is_active=True
    )

    # Today's day
    today = timezone.localdate().strftime("%A")

    # Today's timetable for student's section
    today_timetable = Timetable.objects.filter(
        section=student.section,
        day=today
    ).select_related(
        "subject",
        "staff"
    ).order_by(
        "period"
    )

    context = {
        "student": student,
        "today": today,
        "today_timetable": today_timetable,
    }

    return render(
        request,
        "student_portal/dashboard.html",
        context
    )
@login_required(login_url="login")
def student_profile(request):

    student = Student.objects.select_related(
        "institution",
        "department",
        "course",
        "section"
    ).filter(
        register_no=request.user.username
    ).first()

    if student is None:
        messages.error(
            request,
            "Student profile not found."
        )

        return redirect("student_dashboard")

    context = {
        "student": student,
    }

    return render(
        request,
        "student_portal/profile.html",
        context
    )
@login_required(login_url="login")
def student_subjects(request):

    student = Student.objects.select_related(
        "institution",
        "department",
        "course",
        "section"
    ).filter(
        register_no=request.user.username
    ).first()

    if student is None:
        messages.error(
            request,
            "Student profile not found."
        )

        return redirect("student_dashboard")

    subjects = Subject.objects.select_related(
        "course",
        "staff",
        "department"
    ).filter(
        course=student.course,
        is_active=True
    ).order_by(
        "semester",
        "subject_code"
    )

    context = {
        "student": student,
        "subjects": subjects,
    }

    return render(
        request,
        "student_portal/subjects.html",
        context
    )
@login_required(login_url="login")
def student_materials(request):

    student = Student.objects.select_related(
        "institution",
        "department",
        "course",
        "section"
    ).filter(
        register_no=request.user.username
    ).first()

    if student is None:
        messages.error(
            request,
            "Student profile not found."
        )

        return redirect("student_dashboard")

    materials = StudyMaterial.objects.select_related(
        "staff",
        "subject",
        "section"
    ).filter(
        section=student.section,
        is_active=True
    ).order_by(
        "-created_at"
    )

    context = {
        "student": student,
        "materials": materials,
    }

    return render(
        request,
        "student_portal/materials.html",
        context
    )
@login_required(login_url="login")
def student_assignments(request):

    student = Student.objects.select_related(
        "institution",
        "department",
        "course",
        "section"
    ).filter(
        register_no=request.user.username
    ).first()

    if student is None:
        messages.error(
            request,
            "Student profile not found."
        )

        return redirect("student_dashboard")

    assignments = Assignment.objects.select_related(
        "subject",
        "section",
        "staff"
    ).filter(
        section=student.section,
        is_active=True
    ).order_by(
        "-created_at"
    )

    context = {
        "student": student,
        "assignments": assignments,
    }

    return render(
        request,
        "student_portal/assignments.html",
        context
    )
@login_required(login_url="login")
def student_timetable(request):

    student = Student.objects.select_related(
        "institution",
        "department",
        "course",
        "section"
    ).filter(
        register_no=request.user.username
    ).first()

    if student is None:
        messages.error(
            request,
            "Student profile not found."
        )

        return redirect("student_dashboard")

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    periods = [
        ("1", "Period 1"),
        ("2", "Period 2"),
        ("3", "Period 3"),
        ("4", "Period 4"),
        ("5", "Period 5"),
        ("6", "Period 6"),
    ]

    timetable = Timetable.objects.select_related(
        "subject",
        "staff"
    ).filter(
        section=student.section,
        is_active=True
    )

    timetable_lookup = {
        (entry.day, entry.period): entry
        for entry in timetable
    }

    timetable_rows = []

    for day in days:

        row = {
            "day": day,
            "periods": []
        }

        for period_number, period_name in periods:

            entry = timetable_lookup.get(
                (day, period_number)
            )

            row["periods"].append(entry)

        timetable_rows.append(row)

    context = {
        "student": student,
        "periods": periods,
        "timetable_rows": timetable_rows,
    }

    return render(
        request,
        "student_portal/timetable.html",
        context
    )
@login_required(login_url="login")
def student_attendance(request):

    student = Student.objects.select_related(
        "institution",
        "department",
        "course",
        "section"
    ).filter(
        register_no=request.user.username
    ).first()

    if student is None:

        messages.error(
            request,
            "Student profile not found."
        )

        return redirect("student_dashboard")

    attendance_records = Attendance.objects.select_related(
        "subject",
        "staff",
        "section"
    ).filter(
        student=student
    )

    total_classes = attendance_records.count()

    present_classes = attendance_records.filter(
        status="Present"
    ).count()

    absent_classes = attendance_records.filter(
        status="Absent"
    ).count()

    if total_classes > 0:

        overall_percentage = round(
            (present_classes / total_classes) * 100,
            1
        )

    else:

        overall_percentage = 0


    subjects = attendance_records.values(
        "subject",
        "subject__subject_code",
        "subject__subject_name"
    ).annotate(
        total_classes=Count("id"),
        present_classes=Count(
            "id",
            filter=Q(status="Present")
        ),
        absent_classes=Count(
            "id",
            filter=Q(status="Absent")
        )
    ).order_by(
        "subject__subject_name"
    )


    subject_attendance = []


    for item in subjects:

        total = item["total_classes"]

        present = item["present_classes"]


        if total > 0:

            percentage = round(
                (present / total) * 100,
                1
            )

        else:

            percentage = 0


        if percentage >= 75:

            attendance_status = "Good"

        elif percentage >= 60:

            attendance_status = "Warning"

        else:

            attendance_status = "Low"


        item["percentage"] = percentage

        item["attendance_status"] = attendance_status

        subject_attendance.append(item)


    context = {

        "student": student,

        "total_classes": total_classes,

        "present_classes": present_classes,

        "absent_classes": absent_classes,

        "overall_percentage": overall_percentage,

        "subject_attendance": subject_attendance,

    }


    return render(
        request,
        "student_portal/attendance.html",
        context
    )