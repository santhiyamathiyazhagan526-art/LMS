from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from institution.models import Institution
from department.models import Department
from course.models import Course
from student.models import Student
from staff.models import Staff
from subject.models import Subject 



@login_required(login_url="login")
def dashboard(request):

    context = {

        "institution_count": Institution.objects.count(),

        "department_count": Department.objects.count(),

        "course_count": Course.objects.count(),
        "student_count": Student.objects.count(),
        "staff_count": Staff.objects.count(),   
        "subject_count": Subject.objects.count(), 
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )