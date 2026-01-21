from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DogForm
from .models import Dog
from profiles.models import OwnerProfile


@login_required
def create_dog(request):
    # Vérifier qu'un profil propriétaire existe
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    if owner_profile is None:
        return redirect("create_owner_profile")

    # Empêcher la création de plusieurs chiens (OneToOne)
    if Dog.objects.filter(owner=owner_profile).exists():
        return redirect("home")

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.owner = owner_profile
            dog.save()
            return redirect("home")
    else:
        form = DogForm()

    return render(
        request,
        "dogs/create_dog.html",
        {"form": form}
    )
