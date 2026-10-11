from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Job, JobApplicationField
from .forms import JobForm, JobApplicationFieldForm

from students.models import StudentProfile
from applications.models import Application


def is_admin_user(user):
    return user.is_superuser or user.is_staff


def get_user_role(user):
    try:
        return user.profile.role
    except Exception:
        return None


@login_required
def job_list(request):

    # Student ko admin/TPO job management page access na ho
    if not is_admin_user(request.user):

        role = get_user_role(request.user)

        if role == "student":
            return redirect("student_job_drives")

        if role == "recruiter":
            return redirect("recruiter_dashboard")

        return redirect("student_dashboard")


    jobs = Job.objects.select_related(
        "company"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs
        }
    )


@login_required
def create_job(request):

    # Sirf Admin / TPO
    if not is_admin_user(request.user):

        role = get_user_role(request.user)

        if role == "recruiter":
            return redirect("recruiter_dashboard")

        return redirect("student_dashboard")


    if request.method == "POST":

        form = JobForm(
            request.POST
        )

        if form.is_valid():

            job = form.save()

            messages.success(
                request,
                "Job drive created successfully."
            )

            return redirect(
                "job_form_builder",
                job_id=job.id
            )

    else:
        form = JobForm()


    return render(
        request,
        "jobs/create_job.html",
        {
            "form": form
        }
    )


@login_required
def job_form_builder(request, job_id):

    # Sirf Admin / TPO
    if not is_admin_user(request.user):

        role = get_user_role(request.user)

        if role == "recruiter":
            return redirect("recruiter_dashboard")

        return redirect("student_dashboard")


    job = get_object_or_404(
        Job,
        id=job_id
    )


    custom_fields = JobApplicationField.objects.filter(
        job=job
    ).order_by(
        "order",
        "id"
    )


    if request.method == "POST":

        form = JobApplicationFieldForm(
            request.POST
        )

        if form.is_valid():

            field = form.save(
                commit=False
            )

            field.job = job

            field.save()

            messages.success(
                request,
                "Application field added successfully."
            )

            return redirect(
                "job_form_builder",
                job_id=job.id
            )

    else:

        form = JobApplicationFieldForm()


    return render(
        request,
        "jobs/form_builder.html",
        {
            "job": job,
            "form": form,
            "custom_fields": custom_fields,
        }
    )


@login_required
def delete_job_field(request, field_id):

    # Sirf Admin / TPO
    if not is_admin_user(request.user):

        role = get_user_role(request.user)

        if role == "recruiter":
            return redirect("recruiter_dashboard")

        return redirect("student_dashboard")


    field = get_object_or_404(
        JobApplicationField,
        id=field_id
    )

    job_id = field.job.id


    if request.method == "POST":

        field.delete()

        messages.success(
            request,
            "Application field removed."
        )


    return redirect(
        "job_form_builder",
        job_id=job_id
    )


@login_required
def student_job_drives(request):

    # Admin / TPO ko student job page access nahi
    if is_admin_user(request.user):
        return redirect("admin_dashboard")


    role = get_user_role(
        request.user
    )

    # Recruiter ko student page access nahi
    if role == "recruiter":
        return redirect("recruiter_dashboard")


    student = StudentProfile.objects.filter(
        user=request.user
    ).first()


    # Student profile nahi hai
    if not student:

        messages.warning(
            request,
            "Please complete your student profile first."
        )

        return redirect(
            "student_profile"
        )


    jobs = Job.objects.filter(
        status="active"
    ).select_related(
        "company"
    ).order_by(
        "-created_at"
    )


    student_applications = Application.objects.filter(
        student=student
    )


    jobs_data = []


    for job in jobs:

        eligible = job.is_student_eligible(
            student
        )

        application = student_applications.filter(
            job=job
        ).first()


        jobs_data.append(
            {
                "job": job,
                "eligible": eligible,
                "application": application,
            }
        )


    return render(
        request,
        "jobs/student_job_drives.html",
        {
            "student": student,
            "jobs_data": jobs_data,
        }
    )