from django.db import models
from dogs.models import Dog


class Message(models.Model):
    """Simple message model between two dogs"""
    sender_dog = models.ForeignKey(
        Dog,
        related_name="sent_messages",
        on_delete=models.CASCADE
    )
    receiver_dog = models.ForeignKey(
        Dog,
        related_name="received_messages",
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender_dog.name} → {self.receiver_dog.name}"
