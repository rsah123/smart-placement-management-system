from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "roll_number",
        "branch",
        "cgpa",
        "backlogs",
        "graduation_year",
        "is_placed",
    )

    list_filter = (
        "branch",
        "graduation_year",
        "is_placed",
    )

    search_fields = (
        "user__username",
        "user__email",
        "roll_number",
    )