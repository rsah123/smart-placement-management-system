from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import StudentProfile
from .forms import StudentProfileForm


@login_required
def profile_view(request):
    profile = StudentProfile.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":
        if profile:
            form = StudentProfileForm(
                request.POST,
                request.FILES,
                instance=profile
            )
        else:
            form = StudentProfileForm(
                request.POST,
                request.FILES
            )

        if form.is_valid():
            student_profile = form.save(commit=False)
            student_profile.user = request.user
            student_profile.save()

            messages.success(
                request,
                "Profile saved successfully."
            )

            return redirect("student_profile")

    else:
        form = StudentProfileForm(
            instance=profile
        )

    return render(
        request,
        "students/profile.html",
        {
            "form": form,
            "profile": profile,
        }
    )