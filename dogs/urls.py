from django.urls import path
from .views import create_dog

urlpatterns = [
    path("create/", create_dog, name="create_dog"),
]
