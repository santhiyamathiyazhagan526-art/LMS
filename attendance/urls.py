from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.take_attendance,
        name="take_attendance"
    ),

    path(
        "save/",
        views.save_attendance,
        name="save_attendance"
    ),

    path(
        "report/",
        views.attendance_report,
        name="attendance_report"
    ),

    path(
        "get-years/",
        views.get_years,
        name="get_years"
    ),

    path(
        "get-sections/",
        views.get_sections,
        name="get_sections"
    ),

    path(
        "get-subjects/",
        views.get_subjects,
        name="get_subjects"
    ),

]