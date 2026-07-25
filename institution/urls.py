from django.urls import path
from . import views

urlpatterns = [
    # Institution List
    path("", views.institution_list, name="institution_list"),

    # Add Institution
    path("add/", views.add_institution, name="add_institution"),

    # Edit Institution
    path("edit/<int:id>/", views.edit_institution, name="edit_institution"),
]