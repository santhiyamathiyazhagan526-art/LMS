from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.institution_list,
        name="institution_list"
    ),

    path(
        "edit/<int:id>/",
        views.edit_institution,
        name="edit_institution"
    ),
]