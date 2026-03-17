from django.db import models

from cloudinary.models import CloudinaryField

from profiles.models import OwnerProfile


class Dog(models.Model):
    """Represents a dog profile in the matching system."""

    class Size(models.TextChoices):
        SMALL = "small", "Small"
        MEDIUM = "medium", "Medium"
        LARGE = "large", "Large"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    class EnergyLevel(models.TextChoices):
        COUCH_POTATO = "couch_potato", "🥔 Couch potato"
        CHILL = "chill", "😌 Chill vibes"
        PLAYFUL = "playful", "🎾 Playful"
        ENERGETIC = "energetic", "⚡️ Energetic"
        ZOOMIES = "zoomies", "🚀 Full zoomies"

    owner = models.OneToOneField(
        OwnerProfile,
        on_delete=models.CASCADE,
        related_name="dog",
    )

    profile_photo = CloudinaryField(
        "dog profile photo",
        blank=True,
        null=True,
    )

    name = models.CharField(max_length=100, default="")
    age = models.PositiveIntegerField(null=True, blank=True)
    breed = models.CharField(max_length=100, default="")

    size = models.CharField(
        max_length=10,
        choices=Size.choices,
        blank=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
    )

    energy_level = models.CharField(
        max_length=20,
        choices=EnergyLevel.choices,
        blank=True,
    )

    about_me = models.TextField(
        max_length=150,
        blank=True,
        help_text="Tell us about your dog's personality",
    )

    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dog"
        verbose_name_plural = "Dogs"
        ordering = ["-created_at"]

    def __str__(self):
        """Return string representation of dog profile."""
        return f"{self.name} ({self.owner.name})"

    def get_photo_url(self):
        """
        Generate a Cloudinary URL for the dog's profile photo.

        Returns:
            str | None: Optimized Cloudinary URL for profile photo with
            width=700, height=700, quality=85, or None if no photo available.
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
