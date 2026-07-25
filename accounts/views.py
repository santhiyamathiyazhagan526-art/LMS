from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


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