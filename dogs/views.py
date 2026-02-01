from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import DogForm
from .models import Dog
from profiles.models import OwnerProfile
from connections.models import Connection


@login_required
def create_dog(request):
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    if owner_profile is None:
        owner_profile = OwnerProfile(user=request.user)

    # Check if a dog already exists for this owner;
    # allow update instead of duplicate
    try:
        dog = owner_profile.dog
    except Dog.DoesNotExist:
        dog = None

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner_profile
            instance.save()
            return redirect("browse_dogs")
    else:
        # Pre-populate form if dog exists (edit mode)
        form = DogForm(instance=dog)

    return render(request, "dogs/create_dog.html", {"form": form})


@login_required
def browse_dogs(request):
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    dogs = Dog.objects.all()
    if owner_profile and hasattr(owner_profile, "dog"):
        dogs = dogs.exclude(owner=owner_profile)

    dogs = list(dogs)

    if not dogs:
        return render(request, "dogs/browse_dogs.html", {"dog": None})

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
