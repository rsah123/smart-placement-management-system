from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company",
        "ctc",
        "min_cgpa",
        "max_backlogs",
        "graduation_year",
        "deadline",
        "status",
    )

    list_filter = (
        "status",
        "job_type",
        "graduation_year",
        "company",
    )

    search_fields = (
        "title",
        "company__name",
        "location",
    )