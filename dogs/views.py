from functools import wraps

from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from connections.models import Connection, Dislike
from messaging.models import Message
from profiles.models import OwnerProfile

from .forms import DogForm
from .models import Dog

# Session key constants
SESSION_REGISTRATION_EMAIL = "registration_email"
SESSION_REGISTRATION_PASSWORD = "registration_password"
SESSION_OWNER_PROFILE_ID = "owner_profile_id"
SESSION_OWNER_PROFILE_PHOTO = "owner_profile_photo"
SESSION_DOG_INDEX = "dog_index"
SESSION_SHOW_MATCH_MODAL = "show_match_modal"
SESSION_MATCH_DATA = "match_data"


def require_dog_profile(view_func):
    """
    Decorator that ensures user has both owner profile and dog before
    accessing view.

    Returns:
        Redirect to browse_dogs if requirements not met, otherwise executes
        the decorated view.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        owner_profile = OwnerProfile.objects.filter(user=request.user).first()
        if not owner_profile or not hasattr(owner_profile, "dog"):
            return redirect("browse_dogs")
        return view_func(request, *args, **kwargs)
    return wrapper


def create_dog(request):
    """
    Create a dog profile for the logged-in user during registration.

    Args:
        request: HttpRequest object with POST/GET method for form submission.

    Returns:
        HttpResponse with create_dog.html template or redirect to browse_dogs
        after successful creation and login.

    Raises:
        Redirects to register if session data is missing.
    """
    # Check if we have session data from registration
    if (
        SESSION_REGISTRATION_EMAIL not in request.session
        or SESSION_OWNER_PROFILE_ID not in request.session
    ):
        return redirect("register")

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            # Get session data
            owner_profile_id = request.session.get(SESSION_OWNER_PROFILE_ID)

            # Use existing owner profile created during owner step
            owner_profile = OwnerProfile.objects.get(id=owner_profile_id)
            user = owner_profile.user

            # Create Dog
            dog = form.save(commit=False)
            dog.owner = owner_profile
            dog.save()

            # Clean up session
            del request.session[SESSION_REGISTRATION_EMAIL]
            del request.session[SESSION_REGISTRATION_PASSWORD]
            if SESSION_OWNER_PROFILE_ID in request.session:
                del request.session[SESSION_OWNER_PROFILE_ID]
            if SESSION_OWNER_PROFILE_PHOTO in request.session:
                del request.session[SESSION_OWNER_PROFILE_PHOTO]

            # Log in user
            auth_login(request, user)

            return redirect("browse_dogs")
    else:
        form = DogForm()

    return render(request, "dogs/create_dog.html", {"form": form})


@login_required
def browse_dogs(request):
    """
    Display a scrollable list of dogs for the logged-in user to like or
    dislike.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse with browse_dogs.html template showing next available dog
        or empty state if no more dogs available.
    """
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    dogs = Dog.objects.select_related("owner").all()
    remaining_dogs_count = 0
    if owner_profile and hasattr(owner_profile, "dog"):
        my_dog = owner_profile.dog
        liked_dog_ids = Connection.objects.filter(from_dog=my_dog).values_list(
            "to_dog_id", flat=True
        )
        disliked_dog_ids = Dislike.objects.filter(from_dog=my_dog).values_list(
            "to_dog_id", flat=True
        )
        dogs = (
            dogs.exclude(owner=owner_profile)
            .exclude(id__in=liked_dog_ids)
            .exclude(id__in=disliked_dog_ids)
        )
        remaining_dogs_count = dogs.count()

    dogs = list(dogs)

    # Check if a match modal should be displayed
    match_popup = None
    if request.session.get(SESSION_SHOW_MATCH_MODAL, False):
        match_popup = request.session.pop(SESSION_MATCH_DATA, None)
        request.session.pop(SESSION_SHOW_MATCH_MODAL, False)

    if not dogs:
        return render(
            request,
            "dogs/browse_dogs.html",
            {
                "dog": None,
                "no_more_dogs": True,
                "match_popup": match_popup,
                "remaining_dogs_count": remaining_dogs_count,
            },
        )

    current_index = request.session.get(SESSION_DOG_INDEX, 0)
    if current_index < 0 or current_index >= len(dogs):
        current_index = 0
        request.session[SESSION_DOG_INDEX] = 0

    dog = dogs[current_index]

    if dog.owner.interests:
        dog.owner.interests_list = [
            interest.strip()
            for interest in dog.owner.interests.split(",")
        ]
    else:
        dog.owner.interests_list = []

    return render(
        request,
        "dogs/browse_dogs.html",
        {
            "dog": dog,
            "match_popup": match_popup,
            "remaining_dogs_count": remaining_dogs_count,
        },
    )


@login_required
@require_POST
def next_dog(request):
    """
    Skip current dog and move to next one in the browse queue.

    Args:
        request: HttpRequest object.

    Returns:
        Redirect to browse_dogs with incremented dog_index.
    """
    index = request.session.get(SESSION_DOG_INDEX, 0)
    request.session[SESSION_DOG_INDEX] = index + 1
    return redirect("browse_dogs")


@login_required
@require_POST
@require_dog_profile
@transaction.atomic
def like_dog(request, dog_id):
    """
    Record a like and create bidirectional match connection.

    Args:
        request: HttpRequest object.
        dog_id: ID of the dog being liked.

    Returns:
        Redirect to browse_dogs with match modal data in session.
    """
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    my_dog = owner_profile.dog
    liked_dog = Dog.objects.filter(id=dog_id).first()
    if not liked_dog:
        return redirect("browse_dogs")

    # Create both connections (automatic match)
    Connection.objects.get_or_create(from_dog=my_dog, to_dog=liked_dog)
    Connection.objects.get_or_create(from_dog=liked_dog, to_dog=my_dog)

    # It's always a match now!
    index = request.session.get(SESSION_DOG_INDEX, 0)
    request.session[SESSION_DOG_INDEX] = index + 1

    # Display the match modal
    request.session[SESSION_SHOW_MATCH_MODAL] = True

    # Get photo URLs or None if no photo
    my_dog_photo = my_dog.get_photo_url() if my_dog.profile_photo else None
    other_dog_photo = (
        liked_dog.get_photo_url() if liked_dog.profile_photo else None
    )

    request.session[SESSION_MATCH_DATA] = {
        "my_dog_photo": my_dog_photo,
        "other_dog_photo": other_dog_photo,
        "my_dog_name": my_dog.name,
        "other_dog_name": liked_dog.name,
        "other_dog_id": liked_dog.id,
    }

    return redirect("browse_dogs")


@login_required(login_url="sign_in")
@require_POST
@require_dog_profile
def dislike_dog(request, dog_id):
    """
    Record a dislike (pass) on a dog profile.

    Args:
        request: HttpRequest object.
        dog_id: ID of the dog being disliked.

    Returns:
        Redirect to browse_dogs.
    """
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    my_dog = owner_profile.dog
    disliked_dog = Dog.objects.filter(id=dog_id).first()
    if not disliked_dog:
        return redirect("browse_dogs")

    # Record the dislike
    Dislike.objects.get_or_create(from_dog=my_dog, to_dog=disliked_dog)

    return redirect("browse_dogs")


@login_required(login_url="sign_in")
@require_POST
@require_dog_profile
def reset_matches(request):
    """Clear all matches for the logged-in user's dog and restart discovery."""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    my_dog = owner_profile.dog
    Connection.objects.filter(from_dog=my_dog).delete()
    Dislike.objects.filter(from_dog=my_dog).delete()
    Message.objects.filter(sender_dog=my_dog).delete()
    Message.objects.filter(receiver_dog=my_dog).delete()

    # Reset browsing index to start fresh
    request.session[SESSION_DOG_INDEX] = 0

    return redirect("browse_dogs")
