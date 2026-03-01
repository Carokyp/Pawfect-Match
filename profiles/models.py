from django.contrib.auth.models import User
from django.db import models

from cloudinary.models import CloudinaryField


class OwnerProfile(models.Model):
    """
    Represents an owner profile for a user.

    Attributes:
        user: OneToOneField to User. The associated Django user.
        profile_photo: CloudinaryField. Owner's profile picture.
        name: CharField. Owner's full name.
        age: PositiveIntegerField. Owner's age.
        city: CharField. Owner's city of residence.
        occupation: CharField. Owner's occupation.
        interests: CharField. Comma-separated list of interests.
        about_me: TextField. Personal bio or description.
        created_at: DateTimeField. When profile was created.
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

    def __str__(self):
        """
        Return string representation of owner profile.

        Args:
            None.

        Returns:
            str. Format: "<owner_name> (<user_email>)".
        """
        return f"{self.name} ({self.user.email})"

    def get_photo_url(self):
        """
        Generate a Cloudinary URL for the owner's profile photo.

        Args:
            None.

        Returns:
            str. Optimized Cloudinary URL for profile photo with width=700,
            height=700, quality=85, or None if no photo is available.
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
