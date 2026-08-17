from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Force password change on first login
            if user.must_change_password:
                return redirect("change_password")

            if user.role == "ADMIN":
                return redirect("dashboard")

            elif user.role == "STAFF":
                return redirect("staff_dashboard")

            elif user.role == "STUDENT":
                return redirect("student_dashboard")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "accounts/login.html")


def logout_view(request):

    logout(request)

    return redirect("login")


def forgot_password(request):
    return render(request, "accounts/forgot_password.html")


# ==============================
# ADD THIS BELOW forgot_password()
# ==============================

@login_required
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New password and Confirm password do not match.")
            return redirect("change_password")

        request.user.set_password(new_password)
        request.user.must_change_password = False
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully.")

        if request.user.role == "ADMIN":
            return redirect("dashboard")
        elif request.user.role == "STAFF":
            return redirect("staff_dashboard")
        else:
            return redirect("student_dashboard")

    return render(request, "accounts/change_password.html")