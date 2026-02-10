from django.urls import path
from .views import matches_list, delete_match

urlpatterns = [
    path("matches/", matches_list, name="matches_list"),
    path("delete_match/", delete_match, name="delete_match"),
]
