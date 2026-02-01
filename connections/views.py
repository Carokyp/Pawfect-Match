from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Connection
from dogs.models import Dog
from profiles.models import OwnerProfile


@login_required
def matches_list(request):
    """Affiche la liste des matches (connections bidirectionnelles)"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    
    if not owner_profile or not hasattr(owner_profile, "dog"):
        return render(request, "connections/matches_list.html", {"matches": []})
    
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
            matches_list.append({
                'dog': connection.to_dog,
                'owner': connection.to_dog.owner,
                'matched_at': connection.created_at
            })
    
    return render(request, "connections/matches_list.html", {"matches": matches_list})
