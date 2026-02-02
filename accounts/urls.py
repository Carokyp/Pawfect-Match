from django.urls import path
from .views import register, home, login_view, logout_view, delete_profile

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("sign-in/", login_view, name="sign_in"),
    path("logout/", logout_view, name="logout"),
    path("delete-profile/", delete_profile, name="delete_profile"),
]
