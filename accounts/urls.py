from django.urls import path
from .views import (
    logout_view,
    delete_profile,
)

urlpatterns = [
    path("logout/", logout_view, name="logout"),
    path("delete-profile/", delete_profile, name="delete_profile"),
]
