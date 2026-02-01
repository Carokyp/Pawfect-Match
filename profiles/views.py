from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            
            # Save the profile photo to CloudinaryField temporarily
            # We'll link it to the user when we create the user in create_dog
            temp_owner = form.save(commit=False)
            temp_owner.save()  # Save to get the photo uploaded to Cloudinary
            
            request.session["owner_profile_id"] = temp_owner.id
            request.session["owner_profile_data"] = {
                "name": owner_data["name"],
                "age": owner_data["age"],
                "city": owner_data.get("city", ""),
                "occupation": owner_data.get("occupation", ""),
                "interests": owner_data.get("interests", ""),
                "about_me": owner_data.get("about_me", ""),
            }
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
