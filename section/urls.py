from django.urls import path
from . import views

urlpatterns = [

    path("", views.section_list, name="section_list"),

    path("add/", views.add_section, name="add_section"),

    path("edit/<int:pk>/", views.edit_section, name="edit_section"),

    path("delete/<int:pk>/", views.delete_section, name="delete_section"),

]