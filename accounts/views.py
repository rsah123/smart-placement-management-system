from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegisterForm
from .models import UserProfile


def redirect_user_by_role(user):
    """
    Login ke baad user ko uske correct dashboard par bhejta hai.
    """

    # Django Admin / TPO
    if user.is_superuser or user.is_staff:
        return redirect("admin_dashboard")

    try:
        profile = UserProfile.objects.get(user=user)
        role = profile.role
    except UserProfile.DoesNotExist:
        role = "student"

    if role == "student":
        return redirect("student_dashboard")

    elif role == "recruiter":
        return redirect("recruiter_dashboard")

    elif role == "admin":
        return redirect("admin_dashboard")

    # Unknown role fallback
    return redirect("student_dashboard")


def register_view(request):

    # Already logged-in user ko register page par na rakho
    if request.user.is_authenticated:
        return redirect_user_by_role(request.user)

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data["password"]
            )

            # Normal registration se admin/staff account create na ho
            user.is_staff = False
            user.is_superuser = False

            user.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data["role"]
            )

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    # Agar user already logged in hai
    if request.user.is_authenticated:
        return redirect_user_by_role(request.user)

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:
                messages.error(
                    request,
                    "This account is inactive."
                )

                return render(
                    request,
                    "accounts/login.html"
                )

            login(
                request,
                user
            )

            return redirect_user_by_role(
                user
            )

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")