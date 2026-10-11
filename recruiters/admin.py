from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import RecruiterProfile


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "company",
        "designation",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "company",
    )

    search_fields = (
        "user__username",
        "user__email",
        "company__name",
    )