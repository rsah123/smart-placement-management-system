from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from students.models import StudentProfile
from .models import Interview


def is_admin_user(user):
    return user.is_superuser or user.is_staff


def get_user_role(user):
    try:
        return user.profile.role
    except Exception:
        return None


@login_required
def student_interviews(request):

    # Admin / TPO ko student interview page access nahi
    if is_admin_user(request.user):
        return redirect("admin_dashboard")

    role = get_user_role(request.user)

    # Recruiter ko student page access nahi
    if role == "recruiter":
        return redirect("recruiter_dashboard")

    student = StudentProfile.objects.filter(
        user=request.user
    ).first()

    if not student:
        messages.warning(
            request,
            "Please complete your student profile first."
        )
        return redirect("student_profile")

    interviews = Interview.objects.filter(
        application__student=student
    ).select_related(
        "application",
        "application__job",
        "application__job__company"
    ).order_by(
        "interview_date",
        "interview_time"
    )

    return render(
        request,
        "interviews/student_interviews.html",
        {
            "student": student,
            "interviews": interviews,
        }
    )