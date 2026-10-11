from django.urls import path
from . import views


urlpatterns = [
    path(
        "student/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "recruiter/",
        views.recruiter_dashboard,
        name="recruiter_dashboard"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "placement-stats/",
        views.placement_stats,
        name="placement_stats"
    ),
]