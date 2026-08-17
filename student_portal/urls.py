from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "profile/",
        views.student_profile,
        name="student_profile"
    ),

    path(
        "subjects/",
        views.student_subjects,
        name="student_subjects"
    ),

    path(
        "materials/",
        views.student_materials,
        name="student_materials"
    ),

    path(
        "assignments/",
        views.student_assignments,
        name="student_assignments"
    ),

    path(
        "timetable/",
        views.student_timetable,
        name="student_timetable"
    ),

    path(
        "attendance/",
        views.student_attendance,
        name="student_attendance"
    ),

]