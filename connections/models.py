from django.db import models

from dogs.models import Dog


class Connection(models.Model):
    """
    Represents a "like" connection between two dogs.

    Attributes:
        from_dog: ForeignKey to Dog. The dog who sent the like.
        to_dog: ForeignKey to Dog. The dog who received the like.
        created_at: DateTimeField. Timestamp when connection was created.
    """
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

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["from_dog", "to_dog"],
                name="unique_connection",
            )
        ]

    def __str__(self):
        """
        Return string representation of connection.

        Args:
            None.

        Returns:
            str. Format: "<from_dog_name> ❤️ <to_dog_name>".
        """
        return f"{self.from_dog} ❤️ {self.to_dog}"


class Dislike(models.Model):
    """
    Represents a "dislike" or "pass" action between two dogs.

    Attributes:
        from_dog: ForeignKey to Dog. The dog who sent the dislike.
        to_dog: ForeignKey to Dog. The dog who received the dislike.
        created_at: DateTimeField. Timestamp when dislike was created.
    """
    from_dog = models.ForeignKey(
        Dog,
        related_name="dislikes_given",
        on_delete=models.CASCADE
    )
    to_dog = models.ForeignKey(
        Dog,
        related_name="dislikes_received",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["from_dog", "to_dog"],
                name="unique_dislike",
            )
        ]

    def __str__(self):
        """
        Return string representation of dislike.

        Args:
            None.

        Returns:
            str. Format: "<from_dog_name> 👎🏻 <to_dog_name>".
        """
        return f"{self.from_dog} 👎🏻 {self.to_dog}"
