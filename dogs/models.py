from django.db import models
from cloudinary.models import CloudinaryField
from profiles.models import OwnerProfile


class Dog(models.Model):
    owner = models.OneToOneField(
        OwnerProfile,
        on_delete=models.CASCADE,
        related_name="dog"
    )

    profile_photo = CloudinaryField(
        "dog profile photo",
        blank=True,
        null=True
    )

    name = models.CharField(max_length=100, default="")
    age = models.PositiveIntegerField(null=True, blank=True)
    breed = models.CharField(max_length=100, default="")

    SIZE_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES,
        blank=True
    )

    ENERGY_LEVEL_CHOICES = [
        ('couch_potato', '🥔 Couch potato'),
        ('chill', '😌 Chill vibes'),
        ('playful', '🎾 Playful'),
        ('energetic', '⚡️ Energetic'),
        ('zoomies', '🚀 Full zoomies'),
    ]

    energy_level = models.CharField(
        max_length=20,
        choices=ENERGY_LEVEL_CHOICES,
        blank=True
    )

    about_me = models.TextField(
        max_length=500,
        blank=True,
        help_text="Tell us about your dog's personality"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.owner.name})"

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
