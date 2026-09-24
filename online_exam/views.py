from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import OnlineExam
from subject.models import Subject
from section.models import Section


# ==========================================
# STAFF - ONLINE EXAM LIST
# ==========================================

@login_required
def online_exam_list(request):

    exams = OnlineExam.objects.select_related(
        "subject",
        "section",
        "created_by"
    ).all()

    # Staff should see only exams created by them
    if request.user.role == "STAFF":
        exams = exams.filter(
            created_by=request.user
        )

    context = {
        "exams": exams,
    }

    return render(
        request,
        "online_exam/online_exam_list.html",
        context
    )


# ==========================================
# STAFF - ADD ONLINE EXAM
# ==========================================

@login_required
def add_online_exam(request):

    subjects = Subject.objects.all().order_by("name")

    sections = Section.objects.filter(
        is_active=True
    ).select_related(
        "course",
        "department"
    ).order_by(
        "programme",
        "year",
        "section"
    )

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        subject_id = request.POST.get(
            "subject"
        )

        section_id = request.POST.get(
            "section"
        )

        exam_date = request.POST.get(
            "exam_date"
        )

        start_time = request.POST.get(
            "start_time"
        )

        end_time = request.POST.get(
            "end_time"
        )

        total_marks = request.POST.get(
            "total_marks"
        )

        exam_link = request.POST.get(
            "exam_link",
            ""
        ).strip()

        instructions = request.POST.get(
            "instructions",
            ""
        ).strip()

        # ==========================================
        # VALIDATION
        # ==========================================

        if not title:
            messages.error(
                request,
                "Please enter the exam title."
            )
            return redirect("add_online_exam")

        if not subject_id:
            messages.error(
                request,
                "Please select a subject."
            )
            return redirect("add_online_exam")

        if not section_id:
            messages.error(
                request,
                "Please select a class / section."
            )
            return redirect("add_online_exam")

        if not exam_date:
            messages.error(
                request,
                "Please select the exam date."
            )
            return redirect("add_online_exam")

        if not start_time or not end_time:
            messages.error(
                request,
                "Please select the exam start and end time."
            )
            return redirect("add_online_exam")

        if not total_marks:
            messages.error(
                request,
                "Please enter total marks."
            )
            return redirect("add_online_exam")

        if not exam_link:
            messages.error(
                request,
                "Please enter the online exam link."
            )
            return redirect("add_online_exam")

        # ==========================================
        # GET SUBJECT AND SECTION
        # ==========================================

        subject = get_object_or_404(
            Subject,
            pk=subject_id
        )

        section = get_object_or_404(
            Section,
            pk=section_id,
            is_active=True
        )

        # ==========================================
        # CREATE EXAM
        # ==========================================

        OnlineExam.objects.create(
            title=title,
            subject=subject,
            section=section,
            exam_date=exam_date,
            start_time=start_time,
            end_time=end_time,
            total_marks=total_marks,
            exam_link=exam_link,
            instructions=instructions,
            created_by=request.user,
            is_active=True
        )

        messages.success(
            request,
            "Online exam posted successfully."
        )

        return redirect(
            "online_exam_list"
        )

    context = {
        "subjects": subjects,
        "sections": sections,
    }

    return render(
        request,
        "online_exam/add_online_exam.html",
        context
    )