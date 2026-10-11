from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from students.models import StudentProfile
from .models import Notification


def is_admin_user(user):
    return user.is_superuser or user.is_staff


def get_user_role(user):
    try:
        return user.profile.role
    except Exception:
        return None


@login_required
def student_notifications(request):

    if is_admin_user(request.user):
        return redirect("admin_dashboard")

    role = get_user_role(request.user)

    if role == "recruiter":
        return redirect("recruiter_dashboard")

    student = StudentProfile.objects.filter(
        user=request.user
    ).first()

    if not student:
        return redirect("student_profile")

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "notifications/student_notifications.html",
        {
            "student": student,
            "notifications": notifications,
        }
    )