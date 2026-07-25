from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def staff_dashboard(request):

    context = {

        "subject_count": 0,
        "student_count": 0,
        "today_classes": 0,
        "pending_assignments": 0,

    }

    return render(
        request,
        "staff_panel/dashboard.html",
        context,
    )