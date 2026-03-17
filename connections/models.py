from django.db import models

from dogs.models import Dog


class Like(models.Model):
    """Represents a like between two dogs."""

    from_dog = models.ForeignKey(
        Dog,
        related_name="sent_connections",
        on_delete=models.CASCADE,
    )
    to_dog = models.ForeignKey(
        Dog,
        related_name="received_connections",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "connections_connection"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["from_dog", "to_dog"],
                name="unique_connection",
            ),
        ]

    def __str__(self):
        """Return string representation of like."""
        return f"{self.from_dog} ❤️ {self.to_dog}"


class Dislike(models.Model):
    """Represents a dislike between two dogs."""

    from_dog = models.ForeignKey(
        Dog,
        related_name="dislikes_given",
        on_delete=models.CASCADE,
    )
    to_dog = models.ForeignKey(
        Dog,
        related_name="dislikes_received",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["from_dog", "to_dog"],
                name="unique_dislike",
            ),
        ]

    def __str__(self):
        """Return string representation of dislike."""
        return f"{self.from_dog} 👎🏻 {self.to_dog}"
