from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):

    BRANCH_CHOICES = (
        ("CSE", "Computer Science and Engineering"),
        ("IT", "Information Technology"),
        ("ECE", "Electronics and Communication Engineering"),
        ("EE", "Electrical Engineering"),
        ("ME", "Mechanical Engineering"),
        ("CE", "Civil Engineering"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    roll_number = models.CharField(
        max_length=30,
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    course = models.CharField(
        max_length=50,
        default="B.Tech"
    )

    branch = models.CharField(
        max_length=10,
        choices=BRANCH_CHOICES
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00
    )

    backlogs = models.PositiveIntegerField(
        default=0
    )

    graduation_year = models.PositiveIntegerField()

    # School Details
    tenth_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    twelfth_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    # UG Details
    ug_degree = models.CharField(
        max_length=50,
        blank=True
    )

    ug_specialization = models.CharField(
        max_length=100,
        blank=True
    )

    ug_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True
    )

    ug_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    ug_passing_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    # PG Details
    pg_degree = models.CharField(
        max_length=50,
        blank=True
    )

    pg_specialization = models.CharField(
        max_length=100,
        blank=True
    )

    pg_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True
    )

    pg_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    pg_passing_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    skills = models.TextField(
        blank=True
    )

    job_preference_1 = models.CharField(
        max_length=150,
        blank=True
    )

    job_preference_2 = models.CharField(
        max_length=150,
        blank=True
    )

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    is_placed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"