from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from students.models import StudentProfile
from jobs.models import Job
from applications.models import Application
from interviews.models import Interview
from notifications.models import Notification


def is_admin_user(user):
    return user.is_superuser or user.is_staff


def get_user_role(user):
    try:
        return user.profile.role
    except Exception:
        return None


@login_required
def student_dashboard(request):

    # Admin / TPO ko student dashboard access nahi
    if is_admin_user(request.user):
        return redirect("admin_dashboard")

    role = get_user_role(request.user)

    # Recruiter ko recruiter dashboard
    if role == "recruiter":
        return redirect("recruiter_dashboard")

    student = StudentProfile.objects.filter(
        user=request.user
    ).first()

    eligible_jobs = []

    applications = Application.objects.none()

    interviews = Interview.objects.none()

    profile_completion = 0


    if student:

        all_jobs = Job.objects.filter(
            status="active"
        ).select_related(
            "company"
        ).order_by(
            "-created_at"
        )


        applications = Application.objects.filter(
            student=student
        )


        interviews = Interview.objects.filter(
            application__student=student,
            status="scheduled"
        )


        for job in all_jobs:

            if job.is_student_eligible(student):

                job.current_application = applications.filter(
                    job=job
                ).first()

                eligible_jobs.append(job)


        profile_fields = [
            student.roll_number,
            student.phone,
            student.course,
            student.branch,
            student.cgpa,
            student.graduation_year,
            student.tenth_percentage,
            student.twelfth_percentage,
            student.ug_degree,
            student.ug_specialization,
            student.ug_cgpa,
            student.ug_passing_year,
            student.pg_degree,
            student.pg_specialization,
            student.pg_cgpa,
            student.pg_passing_year,
            student.skills,
            student.job_preference_1,
            student.resume,
        ]


        completed_fields = sum(
            1
            for field in profile_fields
            if field not in [None, "", 0]
        )


        profile_completion = int(
            (
                completed_fields
                / len(profile_fields)
            )
            * 100
        )


    notifications = Notification.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )[:5]


    context = {
        "student": student,
        "profile_completion": profile_completion,
        "eligible_jobs": eligible_jobs[:5],
        "eligible_jobs_count": len(eligible_jobs),
        "applications_count": applications.count(),
        "interviews_count": interviews.count(),
        "notifications": notifications,
    }


    return render(
        request,
        "dashboard/student_dashboard.html",
        context
    )


@login_required
def recruiter_dashboard(request):

    if is_admin_user(request.user):
        return redirect("admin_dashboard")

    role = get_user_role(request.user)

    if role == "student":
        return redirect("student_dashboard")

    return render(
        request,
        "dashboard/recruiter_dashboard.html"
    )


@login_required
def admin_dashboard(request):

    # Sirf Admin / Staff / Superuser
    if not is_admin_user(request.user):

        role = get_user_role(request.user)

        if role == "recruiter":
            return redirect("recruiter_dashboard")

        return redirect("student_dashboard")


    # -------------------------
    # STUDENT COUNTS
    # -------------------------

    total_students = StudentProfile.objects.count()

    placed_students = StudentProfile.objects.filter(
        is_placed=True
    ).count()


    # -------------------------
    # JOB COUNTS
    # -------------------------

    total_jobs = Job.objects.count()

    active_jobs = Job.objects.filter(
        status="active"
    ).count()

    closed_jobs = Job.objects.filter(
        status="closed"
    ).count()


    # -------------------------
    # APPLICATION COUNTS
    # -------------------------

    total_applications = Application.objects.count()

    applied_count = Application.objects.filter(
        status="applied"
    ).count()

    shortlisted_count = Application.objects.filter(
        status="shortlisted"
    ).count()

    interview_stage_count = Application.objects.filter(
        status="interview"
    ).count()

    selected_count = Application.objects.filter(
        status="selected"
    ).count()

    rejected_count = Application.objects.filter(
        status="rejected"
    ).count()


    # -------------------------
    # INTERVIEW COUNTS
    # -------------------------

    scheduled_interviews = Interview.objects.filter(
        status="scheduled"
    ).count()


    # -------------------------
    # RECENT APPLICATIONS
    # -------------------------

    recent_applications = Application.objects.select_related(
        "student",
        "student__user",
        "job",
        "job__company"
    ).order_by(
        "-applied_at"
    )[:8]


    # -------------------------
    # RECENT JOBS
    # -------------------------

    recent_jobs = Job.objects.select_related(
        "company"
    ).order_by(
        "-created_at"
    )[:5]


    context = {
        "total_students": total_students,
        "placed_students": placed_students,

        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "closed_jobs": closed_jobs,

        "total_applications": total_applications,
        "applied_count": applied_count,
        "shortlisted_count": shortlisted_count,
        "interview_stage_count": interview_stage_count,
        "selected_count": selected_count,
        "rejected_count": rejected_count,

        "scheduled_interviews": scheduled_interviews,

        "recent_applications": recent_applications,
        "recent_jobs": recent_jobs,
    }


    return render(
        request,
        "dashboard/admin_dashboard.html",
        context
    )


@login_required
def placement_stats(request):

    # Admin / TPO ko student stats nahi dikhane
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


    applications = Application.objects.filter(
        student=student
    )


    total_applications = applications.count()

    applied_count = applications.filter(
        status="applied"
    ).count()

    shortlisted_count = applications.filter(
        status="shortlisted"
    ).count()

    interview_count = applications.filter(
        status="interview"
    ).count()

    selected_count = applications.filter(
        status="selected"
    ).count()

    rejected_count = applications.filter(
        status="rejected"
    ).count()


    scheduled_interviews = Interview.objects.filter(
        application__student=student,
        status="scheduled"
    ).count()


    context = {
        "student": student,

        "total_applications": total_applications,

        "applied_count": applied_count,

        "shortlisted_count": shortlisted_count,

        "interview_count": interview_count,

        "selected_count": selected_count,

        "rejected_count": rejected_count,

        "scheduled_interviews": scheduled_interviews,
    }


    return render(
        request,
        "dashboard/placement_stats.html",
        context
    )