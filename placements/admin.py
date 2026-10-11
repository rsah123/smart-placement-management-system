from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PlacementRecord


@admin.register(PlacementRecord)
class PlacementRecordAdmin(admin.ModelAdmin):

    list_display = (
        "application",
        "final_ctc",
        "offer_date",
        "joining_date",
    )

    search_fields = (
        "application__student__user__username",
        "application__job__company__name",
    )