from django.urls import path
from .views import matches_list

urlpatterns = [
    path("matches/", matches_list, name="matches_list"),
]
