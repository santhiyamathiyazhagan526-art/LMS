from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.online_exam_list,
        name="online_exam_list"
    ),

    path(
        "add/",
        views.add_online_exam,
        name="add_online_exam"
    ),

]