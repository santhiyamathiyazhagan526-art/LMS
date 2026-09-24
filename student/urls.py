from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # MAIN CLASSES PAGE
    # =====================================================

    path(
        "",
        views.classes,
        name="student_list"
    ),

    path(
        "classes/",
        views.classes,
        name="classes"
    ),


    # =====================================================
    # CLASS STUDENTS
    # =====================================================

    path(
        "classes/<int:section_id>/students/",
        views.class_students,
        name="class_students"
    ),


    # =====================================================
    # ADD STUDENT TO CLASS
    # =====================================================

    path(
        "classes/<int:section_id>/students/add/",
        views.add_student_to_class,
        name="add_student_to_class"
    ),


    # =====================================================
    # ALL STUDENTS
    # =====================================================

    path(
        "all/",
        views.student_list,
        name="all_students"
    ),


    # =====================================================
    # ADD STUDENT
    # =====================================================

    path(
        "add/",
        views.add_student,
        name="add_student"
    ),


    # =====================================================
    # EDIT STUDENT
    # =====================================================

    path(
        "edit/<int:id>/",
        views.edit_student,
        name="edit_student"
    ),


    # =====================================================
    # DELETE STUDENT
    # =====================================================

    path(
        "delete/<int:id>/",
        views.delete_student,
        name="delete_student"
    ),

]