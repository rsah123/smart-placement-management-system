from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from students.models import StudentProfile
from jobs.models import Job
from interviews.models import Interview
from notifications.models import Notification

from .models import Application, ApplicationFieldResponse


def is_management_user(user):
    if user.is_superuser or user.is_staff:
        return True

    try:
        return user.profile.role in ["admin", "recruiter"]
    except Exception:
        return False


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(
        Job.objects.select_related("company"),
        id=job_id,
        status="active"
    )

    student = StudentProfile.objects.filter(
        user=request.user
    ).first()

    if not student:
        messages.error(
            request,
            "Please complete your student profile before applying."
        )
        return redirect("student_profile")

    if not job.is_student_eligible(student):
        messages.error(
            request,
            "You are not eligible for this job drive."
        )
        return redirect("student_dashboard")

    existing_application = Application.objects.filter(
        student=student,
        job=job
    ).first()

    if existing_application:
        messages.info(
            request,
            "You have already applied for this job."
        )

        return redirect(
            "application_detail",
            application_id=existing_application.id
        )

    fields = job.application_fields.all()
    errors = {}

    if request.method == "POST":

        for field in fields:

            if field.field_type == "file":

                uploaded_file = request.FILES.get(
                    field.field_name
                )

                profile_file = None

                if field.prefill_source:
                    profile_file = getattr(
                        student,
                        field.prefill_source,
                        None
                    )

                if (
                    field.required
                    and not uploaded_file
                    and not profile_file
                ):
                    errors[field.field_name] = (
                        f"{field.label} is required."
                    )

            elif field.field_type == "boolean":
                pass

            else:

                value = request.POST.get(
                    field.field_name,
                    ""
                ).strip()

                if field.required and not value:
                    errors[field.field_name] = (
                        f"{field.label} is required."
                    )

        if not errors:

            application = Application.objects.create(
                student=student,
                job=job,
                status="applied"
            )

            for field in fields:

                if field.field_type == "file":

                    uploaded_file = request.FILES.get(
                        field.field_name
                    )

                    response = ApplicationFieldResponse(
                        application=application,
                        field=field
                    )

                    if uploaded_file:
                        response.uploaded_file = uploaded_file

                    elif field.prefill_source:

                        profile_file = getattr(
                            student,
                            field.prefill_source,
                            None
                        )

                        if profile_file:
                            response.value = profile_file.name

                    response.save()

                elif field.field_type == "boolean":

                    value = (
                        "Yes"
                        if request.POST.get(field.field_name)
                        else "No"
                    )

                    ApplicationFieldResponse.objects.create(
                        application=application,
                        field=field,
                        value=value
                    )

                else:

                    value = request.POST.get(
                        field.field_name,
                        ""
                    )

                    ApplicationFieldResponse.objects.create(
                        application=application,
                        field=field,
                        value=value
                    )

            Notification.objects.create(
                user=request.user,
                title="Application Submitted",
                message=(
                    f"Your application for {job.title} "
                    f"at {job.company.name} was submitted successfully."
                )
            )

            messages.success(
                request,
                "Application submitted successfully."
            )

            return redirect("my_applications")

    return render(
        request,
        "applications/apply.html",
        {
            "job": job,
            "student": student,
            "fields": fields,
            "errors": errors,
        }
    )


@login_required
def my_applications(request):

    student = StudentProfile.objects.filter(
        user=request.user
    ).first()

    applications = Application.objects.none()

    if student:
        applications = (
            Application.objects
            .filter(student=student)
            .select_related(
                "job",
                "job__company"
            )
            .order_by("-applied_at")
        )

    return render(
        request,
        "applications/my_applications.html",
        {
            "applications": applications
        }
    )


@login_required
def application_detail(request, application_id):

    application = get_object_or_404(
        Application.objects.select_related(
            "student",
            "student__user",
            "job",
            "job__company"
        ),
        id=application_id
    )

    if (
        not is_management_user(request.user)
        and application.student.user != request.user
    ):
        messages.error(
            request,
            "You are not allowed to view this application."
        )
        return redirect("student_dashboard")

    responses = (
        application.field_responses
        .select_related("field")
        .all()
    )

    return render(
        request,
        "applications/application_detail.html",
        {
            "application": application,
            "responses": responses,
        }
    )


@login_required
def manage_applications(request):

    if not is_management_user(request.user):
        messages.error(
            request,
            "You are not authorized to access this page."
        )
        return redirect("student_dashboard")

    applications = (
        Application.objects
        .select_related(
            "student",
            "student__user",
            "job",
            "job__company"
        )
        .order_by("-applied_at")
    )

    return render(
        request,
        "applications/manage_applications.html",
        {
            "applications": applications
        }
    )


@login_required
def manage_application_detail(request, application_id):

    if not is_management_user(request.user):
        messages.error(
            request,
            "You are not authorized to access this page."
        )
        return redirect("student_dashboard")

    application = get_object_or_404(
        Application.objects.select_related(
            "student",
            "student__user",
            "job",
            "job__company"
        ),
        id=application_id
    )

    responses = (
        application.field_responses
        .select_related("field")
        .all()
    )

    interview = Interview.objects.filter(
        application=application
    ).first()

    return render(
        request,
        "applications/manage_application_detail.html",
        {
            "application": application,
            "responses": responses,
            "interview": interview,
        }
    )


@login_required
def update_application_status(request, application_id):

    if not is_management_user(request.user):
        messages.error(
            request,
            "You are not authorized."
        )
        return redirect("student_dashboard")

    application = get_object_or_404(
        Application,
        id=application_id
    )

    if request.method == "POST":

        new_status = request.POST.get(
            "status"
        )

        allowed_statuses = [
            "applied",
            "shortlisted",
            "interview",
            "selected",
            "rejected",
        ]

        if new_status in allowed_statuses:

            application.status = new_status
            application.save()

            Notification.objects.create(
                user=application.student.user,
                title="Application Status Updated",
                message=(
                    f"Your application for "
                    f"{application.job.title} at "
                    f"{application.job.company.name} "
                    f"is now {application.get_status_display()}."
                )
            )

            if new_status == "selected":
                application.student.is_placed = True
                application.student.save()

            messages.success(
                request,
                "Application status updated successfully."
            )

    return redirect(
        "manage_application_detail",
        application_id=application.id
    )


@login_required
def schedule_interview(request, application_id):

    if not is_management_user(request.user):
        messages.error(
            request,
            "You are not authorized."
        )
        return redirect("student_dashboard")

    application = get_object_or_404(
        Application,
        id=application_id
    )

    if request.method == "POST":

        interview_date = request.POST.get(
            "interview_date"
        )

        interview_time = request.POST.get(
            "interview_time"
        )

        mode = request.POST.get(
            "mode"
        )

        meeting_link = request.POST.get(
            "meeting_link",
            ""
        )

        venue = request.POST.get(
            "venue",
            ""
        )

        remarks = request.POST.get(
            "remarks",
            ""
        )

        Interview.objects.update_or_create(
            application=application,
            defaults={
                "interview_date": interview_date,
                "interview_time": interview_time,
                "mode": mode,
                "meeting_link": meeting_link,
                "venue": venue,
                "remarks": remarks,
                "status": "scheduled",
            }
        )

        application.status = "interview"
        application.save()

        Notification.objects.create(
            user=application.student.user,
            title="Interview Scheduled",
            message=(
                f"Your interview for {application.job.title} "
                f"at {application.job.company.name} "
                f"is scheduled on {interview_date} "
                f"at {interview_time}."
            )
        )

        messages.success(
            request,
            "Interview scheduled successfully."
        )

    return redirect(
        "manage_application_detail",
        application_id=application.id
    )