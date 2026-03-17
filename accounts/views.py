from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from profiles.models import OwnerProfile
from dogs.models import Dog

from .forms import RegisterForm, LoginForm, ForgotPasswordForm

# Auth views


def register(request):
    """
    Handle user registration and redirect to owner profile creation.

    Args:
        request: HttpRequest object with POST/GET method for form submission.

    Returns:
        HttpResponse with register.html template or redirect to
        create_owner_profile.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Check if user already exists (incomplete registration)
            existing_user = User.objects.filter(username=email).first()

            if existing_user:
                # User exists but didn't complete registration
                # Just log them in and redirect to appropriate step
                login(request, existing_user)

                # Check where they left off
                owner_profile = OwnerProfile.objects.filter(
                    user=existing_user
                ).first()

                if not owner_profile:
                    # No owner profile, create empty ones
                    owner_profile = OwnerProfile.objects.create(
                        user=existing_user
                    )
                    Dog.objects.create(owner=owner_profile)
                    return redirect("create_owner_profile")

                if not owner_profile.completed:
                    return redirect("create_owner_profile")

                if hasattr(owner_profile, "dog"):
                    if not owner_profile.dog.completed:
                        return redirect("create_dog")
                else:
                    # No dog, create empty one
                    Dog.objects.create(owner=owner_profile)
                    return redirect("create_dog")

                # Everything completed, go to browse
                return redirect("browse_dogs")
            else:
                # New user - create everything
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )

                # Create empty OwnerProfile (completed=False by default)
                owner_profile = OwnerProfile.objects.create(user=user)

                # Create empty Dog (completed=False by default)
                Dog.objects.create(owner=owner_profile)

                # Log in the user immediately
                login(request, user)

                # Redirect to complete owner profile
                return redirect("create_owner_profile")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """
    Handle user login and redirect to appropriate page based on profile
    completion status.

    Args:
        request: HttpRequest object with POST/GET method for form submission.

    Returns:
        HttpResponse with sign_in.html template or redirect to the appropriate
        page based on completion flags (create_owner_profile, create_dog, or
        browse_dogs).
    """
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Check profile completion and redirect intelligently
            try:
                owner_profile = OwnerProfile.objects.get(user=user)

                # If owner profile not completed, redirect there
                if not owner_profile.completed:
                    return redirect("create_owner_profile")

                # If dog profile not completed, redirect there
                if hasattr(owner_profile, "dog"):
                    if not owner_profile.dog.completed:
                        return redirect("create_dog")
                else:
                    # No dog profile exists, create and redirect
                    return redirect("create_dog")

                # All complete, proceed to browse or next URL
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("browse_dogs")

            except OwnerProfile.DoesNotExist:
                # No owner profile, create empty ones and redirect
                owner_profile = OwnerProfile.objects.create(user=user)
                Dog.objects.create(owner=owner_profile)
                return redirect("create_owner_profile")
    else:
        form = LoginForm()

    return render(request, "accounts/sign_in.html", {"form": form})


def home(request):
    """
    Render the landing page.

    Args:
        request: HttpRequest object for the home page.

    Returns:
        HttpResponse with home.html template.
    """
    return render(request, "accounts/home.html")


@login_required
def logout_view(request):
    """
    Handle user logout.

    Args:
        request: HttpRequest object with POST or GET method.

    Returns:
        Redirect to home page after logout.
    """
    logout(request)
    return redirect("home")


@login_required
def delete_profile(request):
    """
    Delete the current user's owner profile and log them out.

    Args:
        request: HttpRequest object with POST method for deletion.

    Returns:
        Redirect to home after deletion, or view_profile on GET.
    """
    if request.method == "POST":
        user = request.user
        try:
            owner_profile = OwnerProfile.objects.get(user=user)
            owner_profile.delete()
        except OwnerProfile.DoesNotExist:
            pass
        logout(request)
        return redirect("home")
    return redirect("view_profile")

# Error handlers


def handler404(request, exception):
    """Custom 404 error page."""
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """Custom 500 error page."""
    return render(request, "errors/500.html", status=500)


def handler403(request, exception):
    """Custom 403 error page."""
    return render(request, "errors/403.html", status=403)


def handler405(request, exception):
    """Custom 405 error page."""
    return render(request, "errors/405.html", status=405)


def forgot_password(request):
    """
    Reset a user's password without email verification.

    This is a simplified flow intended for development or demos.
    """
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            new_password = form.cleaned_data["new_password"]

            # Update the user's password
            user = User.objects.get(username=email)
            user.set_password(new_password)
            user.save()

            # Redirect to sign in with success message
            return render(request, "accounts/password_reset_success.html")
    else:
        form = ForgotPasswordForm()

    return render(request, "accounts/forgot_password.html", {"form": form})
