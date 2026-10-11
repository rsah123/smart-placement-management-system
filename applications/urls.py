from django.urls import path
from . import views


urlpatterns = [

    # Student routes
    path(
        "apply/<int:job_id>/",
        views.apply_job,
        name="apply_job"
    ),

    path(
        "my/",
        views.my_applications,
        name="my_applications"
    ),

    path(
        "<int:application_id>/",
        views.application_detail,
        name="application_detail"
    ),

    # TPO / Admin routes
    path(
        "manage/all/",
        views.manage_applications,
        name="manage_applications"
    ),

    path(
        "manage/<int:application_id>/",
        views.manage_application_detail,
        name="manage_application_detail"
    ),

    path(
        "manage/<int:application_id>/status/",
        views.update_application_status,
        name="update_application_status"
    ),

    path(
        "manage/<int:application_id>/interview/",
        views.schedule_interview,
        name="schedule_interview"
    ),
]