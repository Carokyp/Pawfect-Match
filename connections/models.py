from django.db import models
from dogs.models import Dog


class Connection(models.Model):
    from_dog = models.ForeignKey(
        Dog,
        related_name="sent_connections",
        on_delete=models.CASCADE
    )
    to_dog = models.ForeignKey(
        Dog,
        related_name="received_connections",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_dog} ❤️ {self.to_dog}"
