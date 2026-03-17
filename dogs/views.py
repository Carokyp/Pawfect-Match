from functools import wraps

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from connections.models import Like, Dislike
from messaging.models import Message
from profiles.models import OwnerProfile
from profiles.views import get_owner_profile, parse_interests

from .forms import DogForm
from .models import Dog


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


@login_required
def create_dog(request):
    """
    Complete the dog profile for the logged-in user during registration.

    Args:
        request: HttpRequest object with POST/GET method for form submission.

    Returns:
        HttpResponse with create_dog.html template or redirect to browse_dogs
        after successful completion.
    """
    owner_profile = get_owner_profile(request.user)
    if not owner_profile:
        return redirect("create_owner_profile")

    dog, _ = Dog.objects.get_or_create(owner=owner_profile)

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.completed = True
            dog.save()
            return redirect("browse_dogs")
    else:
        form = DogForm(instance=dog)

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
    owner_profile = get_owner_profile(request.user)

    dogs = Dog.objects.select_related("owner").filter(
        completed=True,
        owner__completed=True,
    )
    remaining_dogs_count = 0
    if owner_profile and hasattr(owner_profile, "dog"):
        my_dog = owner_profile.dog
        liked_dog_ids = Like.objects.filter(
            from_dog=my_dog,
        ).values_list("to_dog_id", flat=True)
        disliked_dog_ids = Dislike.objects.filter(
            from_dog=my_dog,
        ).values_list("to_dog_id", flat=True)
        dogs = (
            dogs.exclude(owner=owner_profile)
            .exclude(id__in=liked_dog_ids)
            .exclude(id__in=disliked_dog_ids)
        )
        remaining_dogs_count = dogs.count()

    dogs = list(dogs)

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
    dog.owner.interests_list = parse_interests(dog.owner.interests)

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
    owner_profile = get_owner_profile(request.user)
    my_dog = owner_profile.dog
    liked_dog = Dog.objects.filter(id=dog_id).first()
    if not liked_dog:
        return redirect("browse_dogs")

    Like.objects.get_or_create(from_dog=my_dog, to_dog=liked_dog)
    Like.objects.get_or_create(from_dog=liked_dog, to_dog=my_dog)

    index = request.session.get(SESSION_DOG_INDEX, 0)
    request.session[SESSION_DOG_INDEX] = index + 1
    request.session[SESSION_SHOW_MATCH_MODAL] = True
    request.session[SESSION_MATCH_DATA] = {
        "my_dog_photo": (
            my_dog.get_photo_url() if my_dog.profile_photo else None
        ),
        "other_dog_photo": (
            liked_dog.get_photo_url()
            if liked_dog.profile_photo
            else None
        ),
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
    owner_profile = get_owner_profile(request.user)
    my_dog = owner_profile.dog
    disliked_dog = Dog.objects.filter(id=dog_id).first()
    if not disliked_dog:
        return redirect("browse_dogs")

    Dislike.objects.get_or_create(from_dog=my_dog, to_dog=disliked_dog)

    return redirect("browse_dogs")


@login_required(login_url="sign_in")
@require_POST
@require_dog_profile
def reset_matches(request):
    """Clear all matches for the logged-in user's dog and restart discovery."""
    my_dog = get_owner_profile(request.user).dog
    Like.objects.filter(from_dog=my_dog).delete()
    Dislike.objects.filter(from_dog=my_dog).delete()
    Message.objects.filter(sender_dog=my_dog).delete()
    Message.objects.filter(receiver_dog=my_dog).delete()
    request.session[SESSION_DOG_INDEX] = 0
    return redirect("browse_dogs")
