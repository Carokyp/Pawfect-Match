from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from connections.models import Connection, Dislike
from messaging.models import Message
from profiles.models import OwnerProfile

from .forms import DogForm
from .models import Dog


def create_dog(request):
    # Check if we have session data from registration
    if ("registration_email" not in request.session or
            "owner_profile_id" not in request.session):
        return redirect("register")

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            # Get session data
            owner_profile_id = request.session.get("owner_profile_id")

            # Use existing owner profile created during owner step
            owner_profile = OwnerProfile.objects.get(id=owner_profile_id)
            user = owner_profile.user

            # Create Dog
            dog = form.save(commit=False)
            dog.owner = owner_profile
            dog.save()

            # Clean up session
            del request.session["registration_email"]
            del request.session["registration_password"]
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
    remaining_dogs_count = 0
    if owner_profile and hasattr(owner_profile, "dog"):
        my_dog = owner_profile.dog
        liked_dog_ids = Connection.objects.filter(
            from_dog=my_dog
        ).values_list('to_dog_id', flat=True)
        disliked_dog_ids = Dislike.objects.filter(
            from_dog=my_dog
        ).values_list('to_dog_id', flat=True)
        dogs = (
            dogs.exclude(owner=owner_profile)
                .exclude(id__in=liked_dog_ids)
                .exclude(id__in=disliked_dog_ids)
        )
        remaining_dogs_count = dogs.count()

    dogs = list(dogs)

    # Check if a match modal should be displayed
    match_popup = None
    if request.session.get("show_match_modal", False):
        match_popup = request.session.pop("match_data", None)
        request.session.pop("show_match_modal", False)

    if not dogs:
        return render(
            request,
            "dogs/browse_dogs.html",
            {
                "dog": None,
                "no_more_dogs": True,
                "match_popup": match_popup,
                "remaining_dogs_count": remaining_dogs_count
            }
        )

    dog = dogs[0]  # Always the first dog from the filtered list

    if dog.owner.interests:
        dog.owner.interests_list = [i.strip() for i in dog.owner.interests.split(",")]
    else:
        dog.owner.interests_list = []

    return render(request, "dogs/browse_dogs.html", {
        "dog": dog,
        "match_popup": match_popup,
        "remaining_dogs_count": remaining_dogs_count
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

    # Create both connections (automatic match)
    Connection.objects.get_or_create(
        from_dog=my_dog,
        to_dog=liked_dog
    )
    Connection.objects.get_or_create(
        from_dog=liked_dog,
        to_dog=my_dog
    )

    # It's always a match now!
    index = request.session.get("dog_index", 0)
    request.session["dog_index"] = index + 1

    # Display the match modal
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
        "my_dog_name": my_dog.name,
        "other_dog_name": liked_dog.name,
        "other_dog_id": liked_dog.id
    }

    return redirect("browse_dogs")


@login_required(login_url='sign_in')
@require_POST
def dislike_dog(request, dog_id):
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    if not owner_profile or not hasattr(owner_profile, "dog"):
        return redirect("browse_dogs")

    my_dog = owner_profile.dog
    disliked_dog = Dog.objects.get(id=dog_id)

    # Record the dislike
    Dislike.objects.get_or_create(
        from_dog=my_dog,
        to_dog=disliked_dog
    )

    return redirect("browse_dogs")


@login_required(login_url='sign_in')
@require_POST
def reset_matches(request):
    """Clear all matches for the logged-in user's dog and restart discovery."""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    if not owner_profile or not hasattr(owner_profile, "dog"):
        return redirect("browse_dogs")

    my_dog = owner_profile.dog
    Connection.objects.filter(from_dog=my_dog).delete()
    Dislike.objects.filter(from_dog=my_dog).delete()
    Message.objects.filter(sender_dog=my_dog).delete()
    Message.objects.filter(receiver_dog=my_dog).delete()

    return redirect("browse_dogs")
