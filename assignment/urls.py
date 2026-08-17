from django.urls import path

from . import views
from assignment import views as assignment_views


urlpatterns = [

    # ==================================================
    # ASSIGNMENTS
    # ==================================================

    path(
        "",
        assignment_views.assignment_list,
        name="staff_assignments"
    ),

    path(
        "add/",
        assignment_views.add_assignment,
        name="add_assignment"
    ),

    path(
        "edit/<int:id>/",
        assignment_views.edit_assignment,
        name="edit_assignment"
    ),

    path(
        "delete/<int:id>/",
        assignment_views.delete_assignment,
        name="delete_assignment"
    ),

    path(
        "get-years/",
        assignment_views.get_years,
        name="assignment_get_years"
    ),

    path(
        "get-sections/",
        assignment_views.get_sections,
        name="assignment_get_sections"
    ),

]