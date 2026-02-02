from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class OwnerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="owner_profile"
    )

    profile_photo = CloudinaryField(
        "profile photo",
        blank=True,
        null=True
    )

    name = models.CharField(max_length=100, default="")
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, default="")

    occupation = models.CharField(
        max_length=100,
        blank=True
    )

    interests = models.CharField(
        max_length=255,
        blank=True,
    )

    about_me = models.TextField(
        max_length=500,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    def get_photo_url(self):
        if self.profile_photo:
            return self.profile_photo.build_url(
                width=700,
                height=700,
                crop="fill",
                gravity="auto",
                quality=85,
                fetch_format="auto",
            )
        return None
