from django.urls import path
from . import views

urlpatterns = [
    path("", views.take_attendance, name="attendance_list"),
    path("take/", views.take_attendance, name="take_attendance"),
    path("history/", views.attendance_history, name="attendance_history"),

    path(
        "view/<int:subject_id>/<str:attendance_date>/",
        views.view_attendance,
        name="view_attendance",
    ),
    path(
    "edit/<int:subject_id>/<str:attendance_date>/",
    views.edit_attendance,
    name="edit_attendance",
),
    path(
        "delete/<int:subject_id>/<str:attendance_date>/",
        views.delete_attendance,
        name="delete_attendance",
    ),
    path(
    "export/pdf/",
    views.export_attendance_pdf,
    name="export_attendance_pdf"
),
]