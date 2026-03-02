from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from connections.models import Connection
from dogs.models import Dog
from profiles.models import OwnerProfile

from .forms import MessageForm
from .models import Message


def get_user_dog(request, redirect_to="browse_dogs"):
    """
    Helper to retrieve current user's dog profile safely.

    Returns:
        Tuple of (my_dog, redirect_response). If successful, redirect_response
        is None. If error, my_dog is None and redirect_response is a redirect.
    """
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()
    if not owner_profile or not hasattr(owner_profile, "dog"):
        return None, redirect(redirect_to) if redirect_to else None
    return owner_profile.dog, None


@login_required
def messages_inbox(request, dog_id=None):
    """
    Display the messaging inbox with all conversations.

    Args:
        request: HttpRequest object with POST/GET method for message
            submission.
        dog_id: Optional int. If provided, preselect conversation with
            this dog.

    Returns:
        HttpResponse with inbox.html template showing conversation list and
        selected conversation messages. For POST requests, redirects to
        messages_inbox after sending message.
    """
    my_dog, error = get_user_dog(request)
    if error:
        return render(
            request,
            "messages/inbox.html",
            {"conversations": []}
        )

    # Get all messages involving current dog
    conversation_messages = Message.objects.filter(
        Q(sender_dog=my_dog) | Q(receiver_dog=my_dog)
    ).select_related(
        "sender_dog",
        "sender_dog__owner",
        "receiver_dog",
        "receiver_dog__owner",
    )

    # Group by other dog (get latest message per conversation)
    conversations = {}
    for msg in conversation_messages:
        other_dog = (
            msg.receiver_dog
            if msg.sender_dog_id == my_dog.id
            else msg.sender_dog
        )
        other_dog_id = other_dog.id

        if other_dog_id not in conversations:
            conversations[other_dog_id] = {
                "dog": other_dog,
                "owner": other_dog.owner,
                "last_message": msg,
            }

    # Sort by latest message first
    conversations_list = sorted(
        conversations.values(),
        key=lambda x: x["last_message"].created_at,
        reverse=True
    )

    # Load conversation for desktop split view
    # If dog_id provided, use that; otherwise use first conversation
    first_receiver_dog = None
    first_messages = []
    form = None
    is_match = False

    if dog_id:
        # Find conversation with specific dog
        for conv in conversations_list:
            if conv["dog"].id == dog_id:
                first_receiver_dog = conv["dog"]
                break
        # If not in conversations yet, try to get the dog directly
        if not first_receiver_dog:
            first_receiver_dog = Dog.objects.filter(id=dog_id).first()
    elif conversations_list:
        first_receiver_dog = conversations_list[0]["dog"]

    if first_receiver_dog:

        # Check if it's a match
        is_match = Connection.objects.filter(
            from_dog=my_dog,
            to_dog=first_receiver_dog
        ).exists() and Connection.objects.filter(
            from_dog=first_receiver_dog,
            to_dog=my_dog
        ).exists()

        form = MessageForm()

        # Get messages for first conversation
        messages = Message.objects.filter(
            (
                Q(sender_dog=my_dog, receiver_dog=first_receiver_dog)
                | Q(sender_dog=first_receiver_dog, receiver_dog=my_dog)
            )
        ).select_related("sender_dog", "receiver_dog").order_by("created_at")

        for msg in messages:
            sender_avatar = (
                msg.sender_dog.profile_photo.url
                if msg.sender_dog.profile_photo
                else None
            )
            first_messages.append({
                "message": msg,
                "is_sent": msg.sender_dog.id == my_dog.id,
                "sender_avatar": sender_avatar,
                "sender_name": msg.sender_dog.name,
            })

    # Handle message sending from inbox
    if request.method == "POST" and first_receiver_dog:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender_dog = my_dog
            message.receiver_dog = first_receiver_dog
            message.save()
            return redirect(
                "messages_inbox_with_dog",
                dog_id=first_receiver_dog.id
            )

    context = {
        "conversations": conversations_list,
        "first_receiver_dog": first_receiver_dog,
        "first_messages": first_messages,
        "form": form,
        "my_dog": my_dog,
        "is_match": is_match,
    }

    return render(request, "messages/inbox.html", context)


@login_required
def message_thread(request, dog_id):
    """
    Display the full conversation thread with a specific dog.

    Args:
        request: HttpRequest object.
        dog_id: ID of the other dog in the conversation.

    Returns:
        HttpResponse with thread.html template, or redirect if access is not
        allowed.
    """
    my_dog, error = get_user_dog(request)
    if error:
        return error
    receiver_dog = get_object_or_404(Dog, id=dog_id)

    # Check if it's a match
    is_match = Connection.objects.filter(
        from_dog=my_dog,
        to_dog=receiver_dog
    ).exists() and Connection.objects.filter(
        from_dog=receiver_dog,
        to_dog=my_dog
    ).exists()

    if not is_match:
        return redirect("matches_list")

    # Get all messages in this conversation
    messages = Message.objects.filter(
        (
            Q(sender_dog=my_dog, receiver_dog=receiver_dog)
            | Q(sender_dog=receiver_dog, receiver_dog=my_dog)
        )
    ).select_related("sender_dog", "receiver_dog").order_by("created_at")

    # Prepare messages with sender info for template
    messages_with_sender = []
    for msg in messages:
        sender_avatar = (
            msg.sender_dog.profile_photo.url
            if msg.sender_dog.profile_photo
            else None
        )
        messages_with_sender.append({
            "message": msg,
            "is_sent": msg.sender_dog.id == my_dog.id,
            "sender_avatar": sender_avatar,
            "sender_name": msg.sender_dog.name,
        })

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender_dog = my_dog
            message.receiver_dog = receiver_dog
            message.save()
            return redirect("message_thread", dog_id=dog_id)
    else:
        form = MessageForm()

    context = {
        "receiver_dog": receiver_dog,
        "my_dog": my_dog,
        "messages": messages_with_sender,
        "form": form,
        "is_match": is_match
    }

    return render(request, "messages/thread.html", context)


@login_required
@require_POST
def send_message(request, dog_id):
    """
    Send a message to a matched dog from a POST request.

    Args:
        request: HttpRequest object containing message form data.
        dog_id: ID of the message recipient dog.

    Returns:
        JsonResponse for AJAX requests or redirect to message thread.
    """
    my_dog, error = get_user_dog(request)
    if error:
        return error
    receiver_dog = get_object_or_404(Dog, id=dog_id)

    # Check if it's a match
    is_match = Connection.objects.filter(
        from_dog=my_dog,
        to_dog=receiver_dog
    ).exists() and Connection.objects.filter(
        from_dog=receiver_dog,
        to_dog=my_dog
    ).exists()

    if not is_match:
        return redirect("matches_list")

    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender_dog = my_dog
        message.receiver_dog = receiver_dog
        message.save()

        # If AJAX request, return JSON response
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # Get avatar URL for the sent message
            avatar_url = None
            if my_dog.profile_photo:
                avatar_url = my_dog.get_photo_url()
            
            return JsonResponse({
                "success": True,
                "message": {
                    "content": message.content,
                    "time": message.created_at.strftime("%I:%M %p"),
                    "is_sent": True,
                    "avatar": avatar_url
                }
            })

    return redirect("message_thread", dog_id=dog_id)


@login_required
@require_POST
def delete_conversation(request, dog_id):
    """
    Delete all messages between current dog and a specific dog.

    Args:
        request: HttpRequest object.
        dog_id: ID of the other dog in the conversation.

    Returns:
        Redirect to messages_inbox.
    """
    my_dog, error = get_user_dog(request)
    if error:
        return error
    receiver_dog = get_object_or_404(Dog, id=dog_id)

    # Delete all messages between these two dogs (both directions)
    Message.objects.filter(
        (
            Q(sender_dog=my_dog, receiver_dog=receiver_dog)
            | Q(sender_dog=receiver_dog, receiver_dog=my_dog)
        )
    ).delete()

    return redirect("messages_inbox")


@login_required
def get_conversation_messages(request, dog_id):
    """
    Fetch all messages for one conversation as JSON.

    Args:
        request: HttpRequest object.
        dog_id: ID of the other dog in the conversation.

    Returns:
        JsonResponse containing serialized message data, or error JSON if the
        user has no dog profile.
    """
    my_dog, error = get_user_dog(request, redirect_to=None)
    if error:
        return JsonResponse({"error": "No dog profile"}, status=400)
    receiver_dog = get_object_or_404(Dog, id=dog_id)

    # Get all messages in this conversation
    messages = Message.objects.filter(
        (
            Q(sender_dog=my_dog, receiver_dog=receiver_dog)
            | Q(sender_dog=receiver_dog, receiver_dog=my_dog)
        )
    ).select_related("sender_dog", "receiver_dog").order_by("created_at")

    messages_data = []
    for msg in messages:
        messages_data.append({
            "content": msg.content,
            "time": msg.created_at.strftime("%H:%M"),
            "is_sent": msg.sender_dog.id == my_dog.id,
        })

    return JsonResponse({"messages": messages_data})
