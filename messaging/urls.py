from django.urls import path
from . import views

urlpatterns = [
    path("", views.messages_inbox, name="messages_inbox"),
    path("thread/<int:dog_id>/", views.message_thread, name="message_thread"),
    path("send/<int:dog_id>/", views.send_message, name="send_message"),
    path(
        "delete/<int:dog_id>/",
        views.delete_conversation,
        name="delete_conversation"
    ),
]
