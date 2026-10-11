from django.db import models
from companies.models import Company


class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ("full_time", "Full Time"),
        ("internship", "Internship"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("closed", "Closed"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField()

    location = models.CharField(
        max_length=150,
        blank=True
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default="full_time"
    )

    ctc = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="CTC in LPA"
    )

    min_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00
    )

    max_backlogs = models.PositiveIntegerField(
        default=0
    )

    eligible_branches = models.CharField(
        max_length=200,
        help_text="Example: CSE,IT,ECE"
    )

    graduation_year = models.PositiveIntegerField()

    deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def is_student_eligible(self, student):
        branches = [
            branch.strip().upper()
            for branch in self.eligible_branches.split(",")
            if branch.strip()
        ]

        if student.branch.upper() not in branches:
            return False

        if student.cgpa < self.min_cgpa:
            return False

        if student.backlogs > self.max_backlogs:
            return False

        if student.graduation_year != self.graduation_year:
            return False

        return True

    def __str__(self):
        return f"{self.company.name} - {self.title}"


class JobApplicationField(models.Model):

    FIELD_TYPE_CHOICES = (
        ("text", "Text"),
        ("number", "Number"),
        ("email", "Email"),
        ("date", "Date"),
        ("boolean", "Yes / No"),
        ("select", "Dropdown"),
        ("textarea", "Long Text"),
        ("file", "File Upload"),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="application_fields"
    )

    label = models.CharField(
        max_length=150
    )

    field_name = models.SlugField(
        max_length=100
    )

    field_type = models.CharField(
        max_length=20,
        choices=FIELD_TYPE_CHOICES,
        default="text"
    )

    required = models.BooleanField(
        default=True
    )

    options = models.TextField(
        blank=True,
        help_text="For dropdown fields use comma-separated values, e.g. CSE,IT,ECE"
    )

    placeholder = models.CharField(
        max_length=150,
        blank=True
    )

    help_text = models.CharField(
        max_length=250,
        blank=True
    )

    # Example:
    # tenth_percentage
    # twelfth_percentage
    # ug_cgpa
    # pg_cgpa
    # phone
    # resume
    prefill_source = models.CharField(
        max_length=100,
        blank=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order", "id"]

        constraints = [
            models.UniqueConstraint(
                fields=["job", "field_name"],
                name="unique_application_field_per_job"
            )
        ]

    def __str__(self):
        return f"{self.job.title} - {self.label}"