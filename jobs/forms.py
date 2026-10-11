from django import forms
from .models import Job, JobApplicationField


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "company",
            "title",
            "description",
            "location",
            "job_type",
            "ctc",
            "min_cgpa",
            "max_backlogs",
            "eligible_branches",
            "graduation_year",
            "deadline",
            "status",
        ]

        widgets = {
            "company": forms.Select(
                attrs={"class": "form-select"}
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Software Engineer"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Bangalore / Noida / Remote"
                }
            ),
            "job_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "ctc": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "min_cgpa": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "max_backlogs": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "eligible_branches": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "CSE,IT,ECE"
                }
            ),
            "graduation_year": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
        }


class JobApplicationFieldForm(forms.ModelForm):
    class Meta:
        model = JobApplicationField

        fields = [
            "label",
            "field_name",
            "field_type",
            "required",
            "options",
            "placeholder",
            "help_text",
            "prefill_source",
            "order",
        ]

        widgets = {
            "label": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "10th Percentage"
                }
            ),
            "field_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "tenth_percentage"
                }
            ),
            "field_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "required": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "options": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "CSE,IT,ECE"
                }
            ),
            "placeholder": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "help_text": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "prefill_source": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ug_cgpa"
                }
            ),
            "order": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }