from django.urls import path

from . import views


urlpatterns = [

    # Study Material List
    path(
        "",
        views.study_material_list,
        name="study_material_list"
    ),

    # Add Study Material
    path(
        "add/",
        views.add_study_material,
        name="add_study_material"
    ),

    # Delete Study Material
    path(
        "delete/<int:id>/",
        views.delete_study_material,
        name="delete_study_material"
    ),

    # AJAX - Get Years
    path(
        "get-years/",
        views.get_years,
        name="study_material_get_years"
    ),

    # AJAX - Get Sections
    path(
        "get-sections/",
        views.get_sections,
        name="study_material_get_sections"
    ),

]