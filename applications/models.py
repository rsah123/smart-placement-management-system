from django.db import models
from students.models import StudentProfile
from jobs.models import Job, JobApplicationField


class Application(models.Model):

    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview"),
        ("selected", "Selected"),
        ("rejected", "Rejected"),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="applied"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "job"],
                name="unique_student_job_application"
            )
        ]

    def __str__(self):
        return (
            f"{self.student.user.username} - "
            f"{self.job.company.name} - "
            f"{self.job.title}"
        )


class ApplicationFieldResponse(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="field_responses"
    )

    field = models.ForeignKey(
        JobApplicationField,
        on_delete=models.CASCADE,
        related_name="responses"
    )

    value = models.TextField(
        blank=True
    )

    uploaded_file = models.FileField(
        upload_to="application_documents/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["application", "field"],
                name="unique_application_field_response"
            )
        ]

    def __str__(self):
        return (
            f"{self.application.student.user.username} - "
            f"{self.field.label}"
        )