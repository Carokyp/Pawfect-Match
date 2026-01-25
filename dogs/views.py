from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DogForm
from .models import Dog
from profiles.models import OwnerProfile


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

    return render(
        request,
        "dogs/create_dog.html",
        {"form": form}
    )


@login_required
def browse_dogs(request):
    """Display dogs available for matching (all dogs except the user's own dog)."""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    # Get all dogs except the user's own dog
    all_dogs = Dog.objects.all()
    if owner_profile and hasattr(owner_profile, 'dog'):
        all_dogs = all_dogs.exclude(owner=owner_profile)

    return render(
        request,
        "dogs/browse_dogs.html",
        {"dogs": all_dogs}
    )
