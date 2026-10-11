from django.db import models

# Create your models here.
from django.db import models
from applications.models import Application


class Interview(models.Model):

    MODE_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
    )

    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="interview"
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES,
        default="online"
    )

    meeting_link = models.URLField(
        blank=True
    )

    venue = models.CharField(
        max_length=200,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.application.student.user.username} - "
            f"{self.application.job.title}"
        )