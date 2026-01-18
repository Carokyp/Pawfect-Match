from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "accounts/sign_in.html", {"form": form})


def home(request):
    return render(request, "accounts/home.html")
