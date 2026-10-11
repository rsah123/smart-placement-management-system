from django.db import models

# Create your models here.
from django.db import models
from applications.models import Application


class PlacementRecord(models.Model):

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="placement_record"
    )

    offer_date = models.DateField()

    joining_date = models.DateField(
        blank=True,
        null=True
    )

    final_ctc = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Final CTC in LPA"
    )

    offer_letter = models.FileField(
        upload_to="offer_letters/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.application.student.user.username} - "
            f"{self.application.job.company.name}"
        )