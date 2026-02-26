import ast

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from connections.models import Connection
from dogs.forms import DogForm
from dogs.models import Dog

from .forms import OwnerProfileForm
from .models import OwnerProfile


def create_owner_profile(request):
    # Check if email/password are in session (from register)
    if "registration_email" not in request.session:
        return redirect("register")

    if request.method == "POST":
        form = OwnerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Store owner profile data in session
            owner_data = form.cleaned_data.copy()
            interests = owner_data.get("interests")
            if isinstance(interests, (list, tuple)):
                owner_data["interests"] = ", ".join(interests)

            # Create or reuse the user so OwnerProfile has a valid user_id
            email = request.session.get("registration_email")
            password = request.session.get("registration_password")
            user, created = User.objects.get_or_create(
                username=email,
                defaults={"email": email}
            )
            if password:
                user.set_password(password)
                user.save()

            # Create or update OwnerProfile for this user
            owner_profile, _ = OwnerProfile.objects.update_or_create(
                user=user,
                defaults=owner_data,
            )

            request.session["owner_profile_id"] = owner_profile.id
            return redirect("create_dog")
    else:
        form = OwnerProfileForm()

    return render(
        request,
        "profiles/create_owner_profile.html",
        {"form": form}
    )


@login_required
def view_profile(request):
    """View and edit owner profile and dog profile"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile:
        return redirect("create_owner_profile")

    # Get or None for dog
    dog = None
    if hasattr(owner_profile, "dog"):
        dog = owner_profile.dog
    
    def parse_interests(value):
        if not value:
            return []
        value = str(value).strip()
        if value.startswith("[") and value.endswith("]"):
            try:
                parsed = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                parsed = None
            if isinstance(parsed, (list, tuple)):
                return [
                    str(item).strip()
                    for item in parsed
                    if str(item).strip()
                ]
        return [item.strip() for item in value.split(",") if item.strip()]

    owner_profile.interests_list = parse_interests(
        owner_profile.interests
    )

    return render(
        request,
        "profiles/view_profile.html",
        {"owner": owner_profile, "dog": dog}
    )


@login_required
def edit_owner_profile(request):
    """Edit owner profile"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile:
        return redirect("create_owner_profile")

    if request.method == "POST":
        form = OwnerProfileForm(
            request.POST, request.FILES, instance=owner_profile
        )
        if form.is_valid():
            form.save()
            return redirect("view_profile")
    else:
        form = OwnerProfileForm(instance=owner_profile)

    return render(
        request,
        "profiles/edit_owner_profile.html",
        {"form": form}
    )


@login_required
def edit_dog_profile(request):
    """Edit dog profile"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile:
        return redirect("create_owner_profile")

    # Get or create dog
    try:
        dog = owner_profile.dog
    except Dog.DoesNotExist:
        dog = None

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            dog_instance = form.save(commit=False)
            dog_instance.owner = owner_profile
            dog_instance.save()
            return redirect("view_profile")
    else:
        form = DogForm(instance=dog)

    return render(
        request,
        "profiles/edit_dog_profile.html",
        {"form": form}
    )


# Delete profile, dog, and user
@login_required
@require_POST
def delete_profile(request):
    user = request.user
    owner_profile = OwnerProfile.objects.filter(user=user).first()
    if owner_profile:
        # Delete associated dog
        try:
            dog = owner_profile.dog
            # Delete all dog connections
            Connection.objects.filter(from_dog=dog).delete()
            Connection.objects.filter(to_dog=dog).delete()
            dog.delete()
        except Dog.DoesNotExist:
            pass
        # Delete the profile
        owner_profile.delete()
    # Delete the user
    user.delete()
    return redirect("home")
