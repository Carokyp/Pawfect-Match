from django.urls import path
from .views import create_owner_profile

urlpatterns = [
    path("create/", create_owner_profile, name="create_owner_profile"),
]
