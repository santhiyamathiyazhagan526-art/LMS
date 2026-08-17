from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from staff.models import Staff
from student.models import Student
from subject.models import Subject
from timetable.models import Timetable

def staff_dashboard(request):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    # -----------------------------
    # My Subjects
    # -----------------------------
    subject_count = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).count()

    # -----------------------------
    # Staff Courses
    # -----------------------------
    staff_courses = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).values_list(
        "course_id",
        flat=True
    )

    # -----------------------------
    # Students handled by staff
    # -----------------------------
    student_count = Student.objects.filter(
        department=staff.department,
        course_id__in=staff_courses,
        is_active=True
    ).count()

    # -----------------------------
    # Today's Timetable
    # -----------------------------
    today = timezone.localtime(
        timezone.now()
    ).strftime("%A")

    today_timetable = Timetable.objects.filter(
        staff=staff,
        day=today
    ).select_related(
        "section",
        "section__course",
        "subject"
    ).order_by(
        "period"
    )

    today_classes = today_timetable.count()

    # -----------------------------
    # Assignment count
    # -----------------------------
    assignment_count = 0

    # -----------------------------
    # Dashboard
    # -----------------------------
    return render(
        request,
        "staff_panel/dashboard.html",
        {
            "staff": staff,
            "subject_count": subject_count,
            "student_count": student_count,
            "today_classes": today_classes,
            "today_timetable": today_timetable,
            "assignment_count": assignment_count,
        }
    )
def staff_profile(request):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    return render(
        request,
        "staff_panel/profile.html",
        {
            "staff": staff
        }
    )


from subject.models import Subject

def staff_subjects(request):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    subjects = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).select_related(
        "department",
        "course"
    )

    return render(
        request,
        "staff_panel/subjects.html",
        {
            "staff": staff,
            "subjects": subjects,
        }
    )

def staff_students(request):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    # Courses handled by this staff
    staff_courses = Subject.objects.filter(
        staff=staff,
        is_active=True
    ).values_list("course_id", flat=True)
    # Students belonging to staff courses
    students = Student.objects.filter(
        department=staff.department,
        course_id__in=staff_courses,
        is_active=True
    ).select_related(
        "department",
        "course",
        "section"
    ).order_by(
        "programme",
        "year",
        "section__section",
        "register_no"
    )

    total_students = students.count()

    active_students = students.filter(
        is_active=True
    ).count()

    inactive_students = students.filter(
        is_active=False
    ).count()

    return render(
        request,
        "staff_panel/students.html",
        {
            "staff": staff,
            "students": students,
            "total_students": total_students,
            "active_students": active_students,
            "inactive_students": inactive_students,
        }
    )
def staff_student_view(request, pk):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    student = get_object_or_404(
        Student,
        pk=pk
    )

    return render(
        request,
        "staff_panel/student_view.html",
        {
            "staff": staff,
            "student": student,
        }
    )



def staff_attendance(request):
    return redirect("take_attendance")
    return render(
        request,
        "staff_panel/attendance.html",
        {
            "staff": staff
        }
    )


def staff_materials(request):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    return render(
        request,
        "staff_panel/materials.html",
        {
            "staff": staff
        }
    )


def staff_assignments(request):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    return render(
        request,
        "staff_panel/assignments.html",
        {
            "staff": staff
        }
    )


def staff_timetable(request):

    staff = Staff.objects.get(
        staff_id=request.user.username
    )

    return render(
        request,
        "staff_panel/timetable.html",
        {
            "staff": staff
        }
    )


def staff_logout(request):
    return redirect("login")