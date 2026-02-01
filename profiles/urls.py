from django.urls import path
from .views import create_owner_profile, view_profile, edit_owner_profile, edit_dog_profile

urlpatterns = [
    path("create/", create_owner_profile, name="create_owner_profile"),
    path("view/", view_profile, name="view_profile"),
    path("edit/owner/", edit_owner_profile, name="edit_owner_profile"),
    path("edit/dog/", edit_dog_profile, name="edit_dog_profile"),
]
