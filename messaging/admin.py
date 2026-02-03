from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_dog', 'receiver_dog', 'created_at')
    search_fields = ('sender_dog__name', 'receiver_dog__name')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
