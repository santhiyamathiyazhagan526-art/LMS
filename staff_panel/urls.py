from django.urls import path
from . import views
from study_material import views as study_material_views
from assignment import views as assignment_views
from timetable import views as timetable_views

urlpatterns = [

    path('', views.staff_dashboard, name='staff_dashboard'),

    path('profile/', views.staff_profile, name='staff_profile'),

    path('subjects/', views.staff_subjects, name='staff_subjects'),

    path('students/', views.staff_students, name='staff_students'),

    path('attendance/', views.staff_attendance, name='staff_attendance'),

    path('materials/', study_material_views.study_material_list, name='staff_materials'),

     # ==================================================
    # ASSIGNMENTS
    # ==================================================

    path(
        'assignments/',
        assignment_views.assignment_list,
        name='staff_assignments'
    ),

    path(
        'assignments/add/',
        assignment_views.add_assignment,
        name='add_assignment'
    ),

    path(
        'assignments/edit/<int:id>/',
        assignment_views.edit_assignment,
        name='edit_assignment'
    ),

    path(
        'assignments/delete/<int:id>/',
        assignment_views.delete_assignment,
        name='delete_assignment'
    ),

    path(
        'assignments/get-years/',
        assignment_views.get_years,
        name='assignment_get_years'
    ),

    path(
        'assignments/get-sections/',
        assignment_views.get_sections,
        name='assignment_get_sections'
    ),
   path(
    "timetable/",
    timetable_views.timetable_list,
    name="staff_timetable"
),

path(
    "timetable/add/",
    timetable_views.add_timetable,
    name="add_timetable"
),

path(
    "timetable/edit/<int:id>/",
    timetable_views.edit_timetable,
    name="edit_timetable"
),

path(
    "timetable/delete/<int:id>/",
    timetable_views.delete_timetable,
    name="delete_timetable"
),
    path('logout/', views.staff_logout, name='staff_logout'),

    path("students/view/<int:pk>/",
    views.staff_student_view,
    name="staff_student_view",
),

]