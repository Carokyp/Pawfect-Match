from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_POST

from dogs.models import Dog
from profiles.models import OwnerProfile

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
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile or not hasattr(owner_profile, "dog"):
        return render(
            request,
            "connections/matches_list.html",
            {"matches": []}
        )

    my_dog = owner_profile.dog

    # Get all matches (bidirectional connections)
    # Dogs we liked AND who liked us back
    matches = Like.objects.filter(
        from_dog=my_dog
    ).select_related("to_dog", "to_dog__owner")

    # Filter to get only REAL bidirectional connections
    matches_list = []
    for connection in matches:
        # Check if the other dog also created a connection to us
        reverse_connection = Like.objects.filter(
            from_dog=connection.to_dog,
            to_dog=my_dog
        ).exists()

        if reverse_connection:
            owner = connection.to_dog.owner
            if hasattr(owner, 'interests') and owner.interests:
                owner.interests_list = [
                    i.strip() for i in owner.interests.split(",") if i.strip()
                ]
            else:
                owner.interests_list = []
            matches_list.append({
                "dog": connection.to_dog,
                "owner": owner,
                "matched_at": connection.created_at
            })

    return render(
        request,
        "connections/matches_list.html",
        {"matches": matches_list}
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
    dog_id = request.POST.get("dog_id")
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    if not owner_profile or not hasattr(owner_profile, "dog"):
        return HttpResponseForbidden()
    my_dog = owner_profile.dog
    try:
        other_dog = Dog.objects.get(id=dog_id)
    except Dog.DoesNotExist:
        return JsonResponse({"success": False, "error": "Dog not found"})
    # Delete both directions
    Like.objects.filter(from_dog=my_dog, to_dog=other_dog).delete()
    Like.objects.filter(from_dog=other_dog, to_dog=my_dog).delete()
    return JsonResponse({"success": True})
