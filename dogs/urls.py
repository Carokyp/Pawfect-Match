from django.urls import path
from . import views

urlpatterns = [
    path('browse/', views.browse_dogs, name='browse_dogs'),
    path('dislike/<int:dog_id>/', views.dislike_dog, name='dislike_dog'),
    path('create/', views.create_dog, name='create_dog'),
    path('next/', views.next_dog, name='next_dog'),
    path('like/<int:dog_id>/', views.like_dog, name='like_dog'),
    path('reset/', views.reset_matches, name='reset_matches'),
]
