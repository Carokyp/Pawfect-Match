from django.db import models
from profiles.models import OwnerProfile
from cloudinary.models import CloudinaryField

ENERGY_LEVEL_CHOICES = [
    ('couch_potato', '🛋️ Couch potato'),
    ('chill', '😌 Chill vibes'),
    ('playful', '🎾 Playful'),
    ('energetic', '⚡ Energetic'),
    ('zoomies', '🚀 Full zoomies'),
]


class Dog(models.Model):
    owner = models.OneToOneField(
        OwnerProfile,
        on_delete=models.CASCADE,
        related_name="dog"
    )

    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)

    size = models.CharField(
        max_length=10,
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
        ]
    )

    energy_level = models.CharField(
        max_length=12,
        choices=ENERGY_LEVEL_CHOICES
    )

    description = models.TextField(blank=True)

    profile_picture = CloudinaryField('dog picture', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
