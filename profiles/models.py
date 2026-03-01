from django.contrib.auth.models import User
from django.db import models

from cloudinary.models import CloudinaryField


class OwnerProfile(models.Model):
    """
    Owner profile linked one-to-one to a Django user account.

    Stores identity details, profile photo, interests, and a short
    bio used across profile creation, edit, and display views.
    """
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
        max_length=150,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Owner Profile"
        verbose_name_plural = "Owner Profiles"
        ordering = ["-created_at"]

    def __str__(self):
        """Return a readable label combining owner name and user email."""
        return f"{self.name} ({self.user.email})"

    def get_photo_url(self):
        """
        Return an optimized Cloudinary URL for the owner's profile photo.

        Applies standard transformations (700x700, auto gravity, fill crop,
        quality=85, auto format). Returns None when no photo exists.
        """
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
