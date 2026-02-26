from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from dogs.models import Dog
from profiles.models import OwnerProfile

from .forms import RegisterForm, LoginForm, ForgotPasswordForm


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
        except OwnerProfile.DoesNotExist:
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


@login_required
def delete_profile(request):
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


def test_404(request):
    """Test view for 404 page."""
    return render(request, "errors/404.html")


def test_500(request):
    """Test view for 500 page."""
    return render(request, "errors/500.html")


def test_403(request):
    """Test view for 403 page."""
    return render(request, "errors/403.html")


def test_405(request):
    """Test view for 405 page."""
    return render(request, "errors/405.html")


def forgot_password(request):
    """Simple password reset without email verification."""
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
