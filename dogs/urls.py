from django.urls import path
from .views import create_dog, browse_dogs, next_dog, like_dog, reset_matches

urlpatterns = [
    path("create/", create_dog, name="create_dog"),
    path("browse/", browse_dogs, name="browse_dogs"),
    path("next/", next_dog, name="next_dog"),
    path("like/<int:dog_id>/", like_dog, name="like_dog"),
    path("reset/", reset_matches, name="reset_matches"),
]
