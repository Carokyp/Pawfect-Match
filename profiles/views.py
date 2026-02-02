from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import OwnerProfileForm
from .models import OwnerProfile
from dogs.models import Dog
from dogs.forms import DogForm


def create_owner_profile(request):
    # Check if email/password are in session (from register)
    if "registration_email" not in request.session:
        return redirect("register")

    if request.method == "POST":
        form = OwnerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Store owner profile data in session
            owner_data = form.cleaned_data

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
            owner_profile = OwnerProfile.objects.filter(user=user).first()
            if owner_profile:
                for field in [
                    "name",
                    "age",
                    "city",
                    "occupation",
                    "interests",
                    "about_me",
                ]:
                    setattr(owner_profile, field, owner_data.get(field, ""))
                if owner_data.get("profile_photo"):
                    owner_profile.profile_photo = owner_data["profile_photo"]
                owner_profile.save()
            else:
                owner_profile = form.save(commit=False)
                owner_profile.user = user
                owner_profile.save()

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
    
    # Prepare interests as list
    if owner_profile.interests:
        owner_profile.interests_list = [i.strip() for i in owner_profile.interests.split(",")]
    else:
        owner_profile.interests_list = []
    
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
        form = OwnerProfileForm(request.POST, request.FILES, instance=owner_profile)
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
