from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InstitutionForm
from .models import Institution


def institution_list(request):
    """
    Display all institutions.
    """

    institutions = Institution.objects.all().order_by("name")

    context = {
        "institutions": institutions,
    }

    return render(
        request,
        "institution/institution_list.html",
        context
    )


def edit_institution(request, id):
    """
    Edit an existing institution.
    """

    institution = get_object_or_404(
        Institution,
        id=id
    )

    if request.method == "POST":

        form = InstitutionForm(
            request.POST,
            request.FILES,
            instance=institution
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Institution details updated successfully."
            )

            return redirect("institution_list")

    else:

        form = InstitutionForm(
            instance=institution
        )

    context = {
        "form": form,
        "institution": institution,
    }

    return render(
        request,
        "institution/edit_institution.html",
        context
    )