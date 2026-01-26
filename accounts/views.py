from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth.models import User
from profiles.models import OwnerProfile
from dogs.models import Dog


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            login(request, user)
            return redirect("create_owner_profile")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Respect ?next= from @login_required
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            # Otherwise, guide user through onboarding
            owner = OwnerProfile.objects.filter(user=user).first()
            if not owner:
                return redirect("create_owner_profile")

            try:
                _ = owner.dog
                # Dog exists; send to browse_dogs
                return redirect("browse_dogs")
            except Dog.DoesNotExist:
                return redirect("create_dog")
    else:
        form = LoginForm()

    return render(request, "accounts/sign_in.html", {"form": form})


def home(request):
    return render(request, "accounts/home.html")
