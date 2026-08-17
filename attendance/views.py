from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from datetime import date, timedelta

from staff.models import Staff
from subject.models import Subject
from section.models import Section
from student.models import Student

from .models import Attendance


# ==========================================================
# TAKE ATTENDANCE
# ==========================================================

def take_attendance(request):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    # ------------------------------------------
    # Staff subjects
    # ------------------------------------------

    subjects = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).select_related(
        "course"
    )


    # ------------------------------------------
    # Staff department sections
    # ------------------------------------------

    sections = Section.objects.filter(
        department=staff.department,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "course__programme",
        "year",
        "section"
    )


    students = []


    # ------------------------------------------
    # Selected values
    # ------------------------------------------

    selected_programme = request.GET.get(
        "programme",
        ""
    )

    selected_year = request.GET.get(
        "year",
        ""
    )

    selected_section = request.GET.get(
        "section",
        ""
    )

    selected_subject = request.GET.get(
        "subject",
        ""
    )

    selected_date = request.GET.get(
        "date",
        ""
    )


    # ==================================================
    # SHOW STUDENTS
    # ==================================================

    if (
        selected_section
        and selected_subject
        and selected_date
    ):

        students = Student.objects.filter(
            section_id=selected_section,
            is_active=True
        ).order_by(
            "register_no"
        )


    return render(
        request,
        "attendance/take_attendance.html",
        {
            "staff": staff,
            "subjects": subjects,
            "sections": sections,
            "students": students,

            "selected_programme":
                selected_programme,

            "selected_year":
                selected_year,

            "selected_section":
                selected_section,

            "selected_subject":
                selected_subject,

            "selected_date":
                selected_date,
        }
    )


# ==========================================================
# SAVE ATTENDANCE
# ==========================================================

def save_attendance(request):

    if request.method != "POST":
        return redirect("take_attendance")


    # ------------------------------------------
    # Logged-in staff
    # ------------------------------------------

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )


    # ------------------------------------------
    # Submitted values
    # ------------------------------------------

    section_id = request.POST.get(
        "section"
    )

    subject_id = request.POST.get(
        "subject"
    )

    attendance_date = request.POST.get(
        "date"
    )


    # ------------------------------------------
    # Present students
    # ------------------------------------------

    present_students = request.POST.getlist(
        "present_students"
    )


    # ------------------------------------------
    # Validate
    # ------------------------------------------

    if (
        not section_id
        or not subject_id
        or not attendance_date
    ):

        messages.error(
            request,
            "Please select section, subject and date."
        )

        return redirect(
            "take_attendance"
        )


    # ------------------------------------------
    # Get Section
    # ------------------------------------------

    section = get_object_or_404(
        Section,
        id=section_id
    )


    # ------------------------------------------
    # Get Subject
    # ------------------------------------------

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        staff=staff,
        is_active=True
    )


    # ------------------------------------------
    # Get students
    # ------------------------------------------

    students = Student.objects.filter(
        section=section,
        is_active=True
    )


    # ==================================================
    # SAVE PRESENT / ABSENT
    # ==================================================

    for student in students:

        if str(student.id) in present_students:

            status = "Present"

        else:

            status = "Absent"


        Attendance.objects.update_or_create(

            student=student,

            subject=subject,

            attendance_date=attendance_date,

            defaults={
                "staff": staff,
                "section": section,
                "status": status,
            }
        )


    messages.success(
        request,
        "Attendance saved successfully."
    )


    return redirect(
        "attendance_report"
    )


# ==========================================================
# ATTENDANCE REPORT
# ==========================================================

def attendance_report(request):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )


    # ==================================================
    # FILTER VALUES
    # ==================================================

    selected_programme = request.GET.get(
        "programme",
        ""
    )

    selected_year = request.GET.get(
        "year",
        ""
    )

    selected_section = request.GET.get(
        "section",
        ""
    )

    selected_subject = request.GET.get(
        "subject",
        ""
    )

    selected_month = request.GET.get(
        "month",
        ""
    )


    # ==================================================
    # STAFF SUBJECTS
    # ==================================================

    subjects = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).select_related(
        "course"
    )


    # ==================================================
    # STAFF DEPARTMENT SECTIONS
    # ==================================================

    sections = Section.objects.filter(
        department=staff.department,
        is_active=True
    ).select_related(
        "course"
    ).order_by(
        "course__programme",
        "year",
        "section"
    )


    # ==================================================
    # ATTENDANCE QUERY
    # ==================================================

    attendance_records = Attendance.objects.filter(
        staff=staff
    ).select_related(
        "student",
        "subject",
        "section",
        "section__course"
    )


    # ------------------------------------------
    # Programme filter
    # ------------------------------------------

    if selected_programme:

        attendance_records = attendance_records.filter(
            section__course__programme=
                selected_programme
        )


    # ------------------------------------------
    # Year filter
    # ------------------------------------------

    if selected_year:

        attendance_records = attendance_records.filter(
            section__year=selected_year
        )


    # ------------------------------------------
    # Section filter
    # ------------------------------------------

    if selected_section:

        attendance_records = attendance_records.filter(
            section_id=selected_section
        )


    # ------------------------------------------
    # Subject filter
    # ------------------------------------------

    if selected_subject:

        attendance_records = attendance_records.filter(
            subject_id=selected_subject
        )


    # ==================================================
    # MONTH FILTER
    # ==================================================

    if selected_month:

        try:

            year_value, month_value = (
                selected_month.split("-")
            )

            year_value = int(year_value)
            month_value = int(month_value)

            start_date = date(
                year_value,
                month_value,
                1
            )


            # First day of next month
            if month_value == 12:

                next_month = date(
                    year_value + 1,
                    1,
                    1
                )

            else:

                next_month = date(
                    year_value,
                    month_value + 1,
                    1
                )


            end_date = (
                next_month -
                timedelta(days=1)
            )


            attendance_records = attendance_records.filter(
                attendance_date__range=[
                    start_date,
                    end_date
                ]
            )

        except (ValueError, TypeError):

            selected_month = ""


    # ==================================================
    # CREATE REPORT
    # ==================================================

    report_data = []


    # Get unique students from attendance
    student_ids = (
        attendance_records
        .values_list(
            "student_id",
            flat=True
        )
        .distinct()
    )


    students = Student.objects.filter(
        id__in=student_ids
    ).order_by(
        "register_no"
    )


    for student in students:

        student_records = attendance_records.filter(
            student=student
        )


        total_days = student_records.count()


        present_days = student_records.filter(
            status="Present"
        ).count()


        absent_days = student_records.filter(
            status="Absent"
        ).count()


        if total_days > 0:

            percentage = round(
                (
                    present_days /
                    total_days
                ) * 100,
                2
            )

        else:

            percentage = 0


        report_data.append({

            "student": student,

            "total_days":
                total_days,

            "present_days":
                present_days,

            "absent_days":
                absent_days,

            "percentage":
                percentage,
        })


    # ==================================================
    # SUMMARY
    # ==================================================

    total_students = len(
        report_data
    )

    total_present = sum(
        item["present_days"]
        for item in report_data
    )

    total_absent = sum(
        item["absent_days"]
        for item in report_data
    )


    total_attendance = (
        total_present +
        total_absent
    )


    if total_attendance > 0:

        overall_percentage = round(
            (
                total_present /
                total_attendance
            ) * 100,
            2
        )

    else:

        overall_percentage = 0


    # ==================================================
    # CONTEXT
    # ==================================================

    context = {

        "staff":
            staff,

        "subjects":
            subjects,

        "sections":
            sections,

        "report_data":
            report_data,

        "selected_programme":
            selected_programme,

        "selected_year":
            selected_year,

        "selected_section":
            selected_section,

        "selected_subject":
            selected_subject,

        "selected_month":
            selected_month,

        "total_students":
            total_students,

        "total_present":
            total_present,

        "total_absent":
            total_absent,

        "overall_percentage":
            overall_percentage,
    }


    return render(
        request,
        "attendance/report.html",
        context
    )


# ==========================================================
# AJAX : GET YEARS
# ==========================================================

def get_years(request):

    programme = request.GET.get(
        "programme"
    )


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
# AJAX : GET SECTIONS
# ==========================================================

def get_sections(request):

    programme = request.GET.get(
        "programme"
    )

    year = request.GET.get(
        "year"
    )


    sections = Section.objects.filter(

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

        data.append({

            "id":
                section.id,

            "name":
                section.section

        })


    return JsonResponse(
        data,
        safe=False
    )


# ==========================================================
# AJAX : GET SUBJECTS
# ==========================================================

def get_subjects(request):

    staff = get_object_or_404(
        Staff,
        staff_id=request.user.username
    )


    subjects = Subject.objects.filter(
        staff=staff,
        is_active=True
    )


    data = []


    for subject in subjects:

        data.append({

            "id":
                subject.id,

            "name":
                str(subject)

        })


    return JsonResponse(
        data,
        safe=False
    )