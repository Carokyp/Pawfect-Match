from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import DogForm
from .models import Dog
from profiles.models import OwnerProfile
from connections.models import Connection


def create_dog(request):
    # Check if we have session data from registration
    if "registration_email" not in request.session or "owner_profile_data" not in request.session:
        return redirect("register")
    
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            # Get session data
            email = request.session.get("registration_email")
            password = request.session.get("registration_password")
            owner_profile_id = request.session.get("owner_profile_id")
            owner_data = request.session.get("owner_profile_data")
            
            # Create User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            # Update the temp owner profile with the user
            if owner_profile_id:
                owner_profile = OwnerProfile.objects.get(id=owner_profile_id)
                owner_profile.user = user
                owner_profile.save()
            else:
                # Fallback if no temp profile (shouldn't happen)
                owner_profile = OwnerProfile.objects.create(
                    user=user,
                    name=owner_data["name"],
                    age=owner_data["age"],
                    city=owner_data.get("city", ""),
                    occupation=owner_data.get("occupation", ""),
                    interests=owner_data.get("interests", ""),
                    about_me=owner_data.get("about_me", ""),
                )
            
            # Create Dog
            dog = form.save(commit=False)
            dog.owner = owner_profile
            dog.save()
            
            # Clean up session
            del request.session["registration_email"]
            del request.session["registration_password"]
            del request.session["owner_profile_data"]
            if "owner_profile_id" in request.session:
                del request.session["owner_profile_id"]
            if "owner_profile_photo" in request.session:
                del request.session["owner_profile_photo"]
            
            # Log in user
            auth_login(request, user)
            
            return redirect("browse_dogs")
    else:
        form = DogForm()

    return render(request, "dogs/create_dog.html", {"form": form})


@login_required
def browse_dogs(request):
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    dogs = Dog.objects.all()
    if owner_profile and hasattr(owner_profile, "dog"):
        my_dog = owner_profile.dog
        # Exclude own dog and dogs already liked
        liked_dog_ids = Connection.objects.filter(
            from_dog=my_dog
        ).values_list('to_dog_id', flat=True)
        dogs = dogs.exclude(owner=owner_profile).exclude(id__in=liked_dog_ids)

    dogs = list(dogs)

    if not dogs:
        return render(
            request,
            "dogs/browse_dogs.html",
            {"dog": None, "no_more_dogs": True}
        )

    index = request.session.get("dog_index", 0)

    if index >= len(dogs):
        index = 0
        request.session["dog_index"] = 0

    dog = dogs[index]

    if dog.owner.interests:
        dog.owner.interests_list = [i.strip() for i in dog.owner.interests.split(",")]
    else:
        dog.owner.interests_list = []

    # Vérifier si une modal de match doit s'afficher
    match_popup = None
    if request.session.pop("show_match_modal", False):
        match_popup = request.session.pop("match_data", None)

    return render(request, "dogs/browse_dogs.html", {
        "dog": dog,
        "match_popup": match_popup
    })


@login_required
@require_POST
def next_dog(request):
    index = request.session.get("dog_index", 0)
    request.session["dog_index"] = index + 1
    return redirect("browse_dogs")


@login_required
@require_POST
def like_dog(request, dog_id):
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    if not owner_profile or not hasattr(owner_profile, "dog"):
        return redirect("browse_dogs")

    my_dog = owner_profile.dog
    liked_dog = Dog.objects.get(id=dog_id)

    # Créer les deux connections (match automatique)
    Connection.objects.get_or_create(
        from_dog=my_dog,
        to_dog=liked_dog
    )
    Connection.objects.get_or_create(
        from_dog=liked_dog,
        to_dog=my_dog
    )

    # C'est toujours un match maintenant!
    index = request.session.get("dog_index", 0)
    request.session["dog_index"] = index + 1

    # Afficher la modal de match
    request.session["show_match_modal"] = True
    
    # Get photo URLs or None if no photo
    my_dog_photo = (
        my_dog.get_photo_url() if my_dog.profile_photo else None
    )
    other_dog_photo = (
        liked_dog.get_photo_url()
        if liked_dog.profile_photo
        else None
    )
    
    request.session["match_data"] = {
        "my_dog_photo": my_dog_photo,
        "other_dog_photo": other_dog_photo,
        "other_dog_name": liked_dog.name
    }

    return redirect("browse_dogs")


@login_required(login_url='sign_in')
@require_POST
def reset_matches(request):
    """Clear all matches for the logged-in user's dog and restart discovery."""
    owner_profile = getattr(request.user, "owner_profile", None)
    if not owner_profile:
        return redirect("browse_dogs")

    try:
        my_dog = owner_profile.dog
    except Dog.DoesNotExist:
        return redirect("browse_dogs")
    
    # Delete all connections where this dog is the one doing the liking
    Connection.objects.filter(from_dog=my_dog).delete()
    
    # Clear any session match data
    if "match_data" in request.session:
        del request.session["match_data"]
    
    return redirect("browse_dogs")
