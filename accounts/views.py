from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from profiles.models import OwnerProfile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            OwnerProfile.objects.create(
                user=user,
                display_name=user.username
            )

            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def home(request):
    return render(request, "accounts/home.html")
