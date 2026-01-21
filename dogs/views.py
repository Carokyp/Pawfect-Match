from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DogForm
from .models import Dog


@login_required
def create_dog(request):
    owner_profile = request.user.owner_profile

    # Empêcher plusieurs chiens
    if hasattr(owner_profile, "dog"):
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
