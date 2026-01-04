from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class OwnerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    display_name = models.CharField(max_length=50)

    profile_picture = CloudinaryField('profile picture', blank=True, null=True)

    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name
