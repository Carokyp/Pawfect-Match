from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Message model.

    Displays sender, receiver, and creation time in list view with search
    and filtering capabilities. Messages are grouped by conversation.
    """
    list_display = (
        "sender_dog",
        "receiver_dog",
        "content_preview",
        "created_at",
    )
    search_fields = ("sender_dog__name", "receiver_dog__name")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    ordering = ("sender_dog__name", "receiver_dog__name", "created_at")

    def content_preview(self, obj):
        """Return first 50 characters of message content."""
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content

    content_preview.short_description = "Message"
