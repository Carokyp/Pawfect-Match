from django.urls import path
from . import views

urlpatterns = [
    path("", views.messages_inbox, name="messages_inbox"),
    path("<int:dog_id>/", views.messages_inbox, name="messages_inbox_with_dog"),
    path("thread/<int:dog_id>/", views.message_thread, name="message_thread"),
    path("send/<int:dog_id>/", views.send_message, name="send_message"),
    path(
        "delete/<int:dog_id>/",
        views.delete_conversation,
        name="delete_conversation"
    ),
    path(
        "api/<int:dog_id>/",
        views.get_conversation_messages,
        name="get_conversation_messages"
    ),
]
