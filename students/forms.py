from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile

        fields = [
            "roll_number",
            "phone",
            "course",
            "branch",
            "cgpa",
            "backlogs",
            "graduation_year",
            "tenth_percentage",
            "twelfth_percentage",
            "ug_degree",
            "ug_specialization",
            "ug_cgpa",
            "ug_percentage",
            "ug_passing_year",
            "pg_degree",
            "pg_specialization",
            "pg_cgpa",
            "pg_percentage",
            "pg_passing_year",
            "skills",
            "job_preference_1",
            "job_preference_2",
            "resume",
        ]

        widgets = {
            "roll_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "course": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "branch": forms.Select(
                attrs={"class": "form-select"}
            ),
            "cgpa": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "backlogs": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "graduation_year": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "tenth_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "twelfth_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "ug_degree": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "ug_specialization": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "ug_cgpa": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "ug_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "ug_passing_year": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "pg_degree": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "pg_specialization": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "pg_cgpa": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "pg_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "pg_passing_year": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "skills": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Python, Django, SQL, Machine Learning..."
                }
            ),
            "job_preference_1": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "job_preference_2": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "resume": forms.FileInput(
                attrs={"class": "form-control"}
            ),
        }