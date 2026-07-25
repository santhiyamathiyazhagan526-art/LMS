from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Institution
from .forms import InstitutionForm


# ===========================
# Institution List
# ===========================
@login_required(login_url="login")
def institution_list(request):

    institutions = Institution.objects.all()

    context = {
        "institutions": institutions
    }

    return render(
        request,
        "institution/institution_list.html",
        context
    )


# ===========================
# Add Institution
# ===========================
@login_required(login_url="login")
def add_institution(request):

    if request.method == "POST":

        form = InstitutionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("institution_list")

    else:

        form = InstitutionForm()

    context = {
        "form": form,
        "title": "Add Institution",
        "button": "Save Institution"
    }

    return render(
        request,
        "institution/institution_form.html",
        context
    )


# ===========================
# Edit Institution
# ===========================
@login_required(login_url="login")
def edit_institution(request, id):

    institution = get_object_or_404(Institution, id=id)

    if request.method == "POST":

        form = InstitutionForm(
            request.POST,
            request.FILES,
            instance=institution
        )

        if form.is_valid():
            form.save()
            return redirect("institution_list")

    else:

        form = InstitutionForm(instance=institution)

    context = {
        "form": form,
        "title": "Edit Institution",
        "button": "Update Institution"
    }

    return render(
        request,
        "institution/institution_form.html",
        context
    )
