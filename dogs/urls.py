from django.urls import path
from .views import create_dog, browse_dogs

urlpatterns = [
    path("create/", create_dog, name="create_dog"),
    path("browse/", browse_dogs, name="browse_dogs"),
]
