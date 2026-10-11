from django.urls import path
from . import views


urlpatterns = [

    # Admin / TPO Job Drives
    path(
        "",
        views.job_list,
        name="job_list"
    ),

    # Create Job
    path(
        "create/",
        views.create_job,
        name="create_job"
    ),

    # Student Job Drives
    path(
        "student/",
        views.student_job_drives,
        name="student_job_drives"
    ),

    # Application Form Builder
    path(
        "<int:job_id>/form-builder/",
        views.job_form_builder,
        name="job_form_builder"
    ),

    # Delete Dynamic Field
    path(
        "field/<int:field_id>/delete/",
        views.delete_job_field,
        name="delete_job_field"
    ),
]