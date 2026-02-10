from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
from .models import Connection
from profiles.models import OwnerProfile
from dogs.models import Dog


@login_required
def matches_list(request):
    """Affiche la liste des matches (connections bidirectionnelles)"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile or not hasattr(owner_profile, "dog"):
        return render(
            request,
            "connections/matches_list.html",
            {"matches": []}
        )

    my_dog = owner_profile.dog

    # Récupérer tous les matches (connections bidirectionnelles)
    # Les chiens qu'on a liké ET qui nous ont liké
    matches = Connection.objects.filter(
        from_dog=my_dog
    ).select_related('to_dog', 'to_dog__owner')

    # Filtrer pour avoir que les VRAIES connections bidirectionnelles
    matches_list = []
    for connection in matches:
        # Vérifier que l'autre chien a aussi créé une connection vers nous
        reverse_connection = Connection.objects.filter(
            from_dog=connection.to_dog,
            to_dog=my_dog
        ).exists()
        
        if reverse_connection:
            owner = connection.to_dog.owner
            if hasattr(owner, 'interests') and owner.interests:
                owner.interests_list = [i.strip() for i in owner.interests.split(',') if i.strip()]
            else:
                owner.interests_list = []
            matches_list.append({
                'dog': connection.to_dog,
                'owner': owner,
                'matched_at': connection.created_at
            })

    return render(
        request,
        "connections/matches_list.html",
        {"matches": matches_list}
    )


@login_required
@require_POST
def delete_match(request):
    """Supprime la connexion entre deux chiens (match)"""
    dog_id = request.POST.get('dog_id')
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    if not owner_profile or not hasattr(owner_profile, "dog"):
        return HttpResponseForbidden()
    my_dog = owner_profile.dog
    try:
        other_dog = Dog.objects.get(id=dog_id)
    except Dog.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dog not found'})
    # Delete both directions
    Connection.objects.filter(from_dog=my_dog, to_dog=other_dog).delete()
    Connection.objects.filter(from_dog=other_dog, to_dog=my_dog).delete()
    return JsonResponse({'success': True})
