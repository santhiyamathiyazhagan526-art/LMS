from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from student.models import Student


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        User = get_user_model()

        # ==========================================
        # STEP 1: CHECK USERNAME EXISTS
        # ==========================================

        try:
            user_record = User.objects.get(username=username)
        except User.DoesNotExist:

            messages.error(
                request,
                "Invalid Username or Password."
            )

            return render(
                request,
                "accounts/login.html"
            )

        # ==========================================
        # STEP 2: STUDENT VALIDATION
        # ==========================================

        if user_record.role == "STUDENT":

            student_exists = Student.objects.filter(
                register_no=username,
                is_active=True
            ).exists()

            if not student_exists:

                messages.error(
                    request,
                    "Invalid Register Number or Password."
                )

                return render(
                    request,
                    "accounts/login.html"
                )

        # ==========================================
        # STEP 3: CHECK PASSWORD
        # ==========================================

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            messages.error(
                request,
                "Invalid Username or Password."
            )

            return render(
                request,
                "accounts/login.html"
            )

        # ==========================================
        # STEP 4: LOGIN
        # ==========================================

        login(request, user)

        # ==========================================
        # STEP 5: FORCE PASSWORD CHANGE
        # ==========================================

        if user.must_change_password:

            return redirect("change_password")

        # ==========================================
        # STEP 6: ROLE REDIRECT
        # ==========================================

        if user.role == "ADMIN":

            return redirect("dashboard")

        elif user.role == "STAFF":

            return redirect("staff_dashboard")

        elif user.role == "STUDENT":

            return redirect("student_dashboard")

        else:

            logout(request)

            messages.error(
                request,
                "Invalid user role."
            )

            return render(
                request,
                "accounts/login.html"
            )

    return render(
        request,
        "accounts/login.html"
    )
# ==========================================
# LOGOUT
# ==========================================

def logout_view(request):

    logout(request)

    return redirect("login")


# ==========================================
# FORGOT / RESET PASSWORD
# ==========================================

def forgot_password(request):

    if request.method == "POST":

        # Get form values
        username = request.POST.get(
            "username",
            ""
        ).strip()

        register_no = request.POST.get(
            "register_no",
            ""
        ).strip()

        new_password = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )


        # ------------------------------------------
        # Check all fields
        # ------------------------------------------

        if (
            not username
            or not register_no
            or not new_password
            or not confirm_password
        ):

            messages.error(
                request,
                "Please fill in all fields."
            )

            return redirect("forgot_password")


        # ------------------------------------------
        # Check password match
        # ------------------------------------------

        if new_password != confirm_password:

            messages.error(
                request,
                "New password and Confirm password do not match."
            )

            return redirect("forgot_password")


        # ------------------------------------------
        # Check minimum password length
        # ------------------------------------------

        if len(new_password) < 8:

            messages.error(
                request,
                "Password must contain at least 8 characters."
            )

            return redirect("forgot_password")


        # ------------------------------------------
        # Get custom User model
        # ------------------------------------------

        User = get_user_model()


        # ------------------------------------------
        # Find student User account
        # ------------------------------------------

        try:

            user = User.objects.get(
                username=username,
                role="STUDENT"
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Invalid username or register number."
            )

            return redirect("forgot_password")


        # ------------------------------------------
        # Find Student record
        # ------------------------------------------

        try:

            student = Student.objects.get(
                register_no=register_no
            )

        except Student.DoesNotExist:

            messages.error(
                request,
                "Invalid username or register number."
            )

            return redirect("forgot_password")


        # ------------------------------------------
        # Verify username and register number
        # ------------------------------------------

        if user.username != student.register_no:

            messages.error(
                request,
                "Username and register number do not match."
            )

            return redirect("forgot_password")


        # ------------------------------------------
        # Check student account status
        # ------------------------------------------

        if not student.is_active:

            messages.error(
                request,
                "This student account is inactive. Please contact the administrator."
            )

            return redirect("forgot_password")


        # ------------------------------------------
        # Set new password
        # ------------------------------------------

        user.set_password(new_password)

        # Password reset completed
        user.must_change_password = False

        user.save()


        # ------------------------------------------
        # Success message
        # ------------------------------------------

        messages.success(
            request,
            "Password reset successfully. You can now login with your new password."
        )

        return redirect("login")


    # ------------------------------------------
    # GET request
    # ------------------------------------------

    return render(
        request,
        "accounts/forgot_password.html"
    )


# ==========================================
# CHANGE PASSWORD
# ==========================================

@login_required
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get(
            "current_password",
            ""
        )

        new_password = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )


        # ------------------------------------------
        # Check current password
        # ------------------------------------------

        if not request.user.check_password(
            current_password
        ):

            messages.error(
                request,
                "Current password is incorrect."
            )

            return redirect("change_password")


        # ------------------------------------------
        # Check new password match
        # ------------------------------------------

        if new_password != confirm_password:

            messages.error(
                request,
                "New password and Confirm password do not match."
            )

            return redirect("change_password")


        # ------------------------------------------
        # Check minimum password length
        # ------------------------------------------

        if len(new_password) < 8:

            messages.error(
                request,
                "Password must contain at least 8 characters."
            )

            return redirect("change_password")


        # ------------------------------------------
        # Update password
        # ------------------------------------------

        request.user.set_password(
            new_password
        )

        request.user.must_change_password = False

        request.user.save()


        # Keep user logged in
        update_session_auth_hash(
            request,
            request.user
        )


        # ------------------------------------------
        # Success message
        # ------------------------------------------

        messages.success(
            request,
            "Password changed successfully."
        )


        # ------------------------------------------
        # Redirect according to role
        # ------------------------------------------

        if request.user.role == "ADMIN":

            return redirect("dashboard")

        elif request.user.role == "STAFF":

            return redirect("staff_dashboard")

        else:

            return redirect("student_dashboard")


    return render(
        request,
        "accounts/change_password.html"
    )