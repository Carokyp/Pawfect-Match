from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OwnerProfileForm
from .models import OwnerProfile


@login_required
def create_owner_profile(request):
    # Empêcher la création de plusieurs profils
    if OwnerProfile.objects.filter(user=request.user).exists():
        return redirect("create_dog")

    if request.method == "POST":
        form = OwnerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            owner_profile = form.save(commit=False)
            owner_profile.user = request.user
            owner_profile.save()
            return redirect("create_dog")
    else:
        form = OwnerProfileForm()

    return render(
        request,
        "profiles/create_owner_profile.html",
        {"form": form}
    )
