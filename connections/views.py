from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from dogs.models import Dog
from profiles.views import get_owner_profile, parse_interests

from .models import Like


@login_required
def matches_list(request):
    """
    Display the list of bidirectional matches (mutual likes).

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse with matches_list.html template showing all matched dogs
        with owner information.
    """
    owner_profile = get_owner_profile(request.user)

    if not owner_profile or not hasattr(owner_profile, "dog"):
        return render(
            request,
            "connections/matches_list.html",
            {"matches": []},
        )

    my_dog = owner_profile.dog
    liked = Like.objects.filter(
        from_dog=my_dog,
    ).select_related("to_dog", "to_dog__owner")
    liked_back_ids = Like.objects.filter(
        to_dog=my_dog,
    ).values_list("from_dog_id", flat=True)

    matches = []
    for connection in liked:
        if connection.to_dog_id not in liked_back_ids:
            continue
        owner = connection.to_dog.owner
        owner.interests_list = parse_interests(owner.interests)
        matches.append({
            "dog": connection.to_dog,
            "owner": owner,
            "matched_at": connection.created_at,
        })

    return render(
        request,
        "connections/matches_list.html",
        {"matches": matches},
    )


@login_required
@require_POST
def delete_match(request):
    """
    Delete a match between two dogs.

    Args:
        request: HttpRequest object with POST method containing dog_id.

    Returns:
        JsonResponse with success status.

    Raises:
        Returns HttpResponseForbidden if user has no dog profile.
        Returns JsonResponse with error if dog_id not found.
    """
    owner_profile = get_owner_profile(request.user)
    if not owner_profile or not hasattr(owner_profile, "dog"):
        return HttpResponseForbidden()

    dog_id = request.POST.get("dog_id")
    my_dog = owner_profile.dog

    try:
        other_dog = Dog.objects.get(id=dog_id)
    except Dog.DoesNotExist:
        return JsonResponse({"success": False, "error": "Dog not found"})

    Like.objects.filter(from_dog=my_dog, to_dog=other_dog).delete()
    Like.objects.filter(from_dog=other_dog, to_dog=my_dog).delete()

    return JsonResponse({"success": True})
