from django.urls import path
from .views import register, home, login_view

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("sign-in/", login_view, name="sign_in"),
]
