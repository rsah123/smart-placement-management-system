from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "job",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "job__company",
    )

    search_fields = (
        "student__user__username",
        "student__roll_number",
        "job__title",
        "job__company__name",
    )