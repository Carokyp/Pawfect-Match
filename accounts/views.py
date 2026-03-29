from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect

from profiles.models import OwnerProfile
from dogs.models import Dog

from .forms import RegisterForm, LoginForm, ForgotPasswordForm


# Helpers


def get_profile_redirect(owner_profile):
    """
    Return the correct URL name based on the user's registration progress.

    Checks owner profile and dog profile completion in order,
    returning the first incomplete step.

    Returns:
        str: URL name to redirect to.
    """
    if not owner_profile.completed:
        return "create_owner_profile"

    if not hasattr(owner_profile, "dog"):
        return "create_dog"

    if not owner_profile.dog.completed:
        return "create_dog"

    return "browse_dogs"


def get_or_create_profiles(user):
    """
    Ensure a user has both an owner profile and a dog profile.

    Creates missing profiles with default values if they don't exist.

    Returns:
        OwnerProfile: The user's owner profile.
    """
    owner_profile, _ = OwnerProfile.objects.get_or_create(user=user)

    if not hasattr(owner_profile, "dog"):
        Dog.objects.create(owner=owner_profile)

    return owner_profile


# Auth views


def register(request):
    """
    Handle user registration.

    Creates a new user with empty profiles on first registration.
    Resumes incomplete registration if the user already exists.

    Returns:
        HttpResponse: register.html or redirect to the next registration step.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            existing_user = User.objects.filter(username=email).first()

            if existing_user:
                # User exists but never finished registration — resume it
                login(request, existing_user)
                owner_profile = get_or_create_profiles(existing_user)
            else:
                # New user — create account and empty profiles
                existing_user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                )
                owner_profile = get_or_create_profiles(existing_user)
                login(request, existing_user)

            return redirect(get_profile_redirect(owner_profile))
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """
    Handle user login.

    Redirects to the correct page based on profile completion.
    Supports ?next= parameter to return the user to their intended page.

    Returns:
        HttpResponse: sign_in.html or redirect to the appropriate page.
    """
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            owner_profile = get_or_create_profiles(user)
            redirect_url = get_profile_redirect(owner_profile)

            # If profiles are complete, respect the ?next= parameter
            if redirect_url == "browse_dogs":
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)

            return redirect(redirect_url)
    else:
        form = LoginForm()

    return render(request, "accounts/sign_in.html", {"form": form})


def home(request):
    """Render the landing page."""
    return render(request, "accounts/home.html")


@login_required
def logout_view(request):
    """Log out the current user and redirect to home."""
    logout(request)
    return redirect("home")


@login_required
def delete_profile(request):
    """
    Delete the current user's profile and log them out.

    Only processes DELETE on POST requests.

    Returns:
        HttpResponse: Redirect to home after deletion, or view_profile on GET.
    """
    if request.method == "POST":
        try:
            OwnerProfile.objects.get(user=request.user).delete()
        except OwnerProfile.DoesNotExist:
            pass

        logout(request)
        return redirect("home")

    return redirect("view_profile")


def forgot_password(request):
    """
    Reset a user's password.

    Returns:
        HttpResponse: forgot_password.html or password_reset_success.html.
    """
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            new_password = form.cleaned_data["new_password"]

            user = User.objects.get(username=email)
            user.set_password(new_password)
            user.save()

            return render(request, "accounts/password_reset_success.html")
    else:
        form = ForgotPasswordForm()

    return render(request, "accounts/forgot_password.html", {"form": form})


# Error handlers


def handler404(request, exception):
    """Render custom 404 page."""
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """Render custom 500 page."""
    return render(request, "errors/500.html", status=500)


def handler403(request, exception):
    """Render custom 403 page."""
    return render(request, "errors/403.html", status=403)


def handler405(request, exception):
    """Render custom 405 error page."""
    return render(request, "errors/405.html", status=405)
