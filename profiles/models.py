from django.db import models
from django.contrib.auth.models import User


class OwnerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    display_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name
