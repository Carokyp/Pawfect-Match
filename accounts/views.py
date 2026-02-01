from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .forms import LoginForm
from profiles.models import OwnerProfile
from dogs.models import Dog


def register(request):
    # Clean up session from previous registration attempt
    if "registration_email" in request.session:
        del request.session["registration_email"]
    if "registration_password" in request.session:
        del request.session["registration_password"]
    if "owner_profile_data" in request.session:
        del request.session["owner_profile_data"]
    if "owner_profile_photo" in request.session:
        del request.session["owner_profile_photo"]
    if "owner_profile_id" in request.session:
        # Delete the temp owner profile if it exists
        owner_id = request.session["owner_profile_id"]
        try:
            OwnerProfile.objects.get(id=owner_id).delete()
        except:
            pass
        del request.session["owner_profile_id"]
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Store email and password in session (don't create User yet)
            request.session["registration_email"] = form.cleaned_data["email"]
            request.session["registration_password"] = form.cleaned_data["password"]
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


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return redirect("home")
