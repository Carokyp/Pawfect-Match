from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from connections.models import Like
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


def is_match(dog_a, dog_b):
    """Return True if dog_a and dog_b have mutually liked each other."""
    return (
        Like.objects.filter(from_dog=dog_a, to_dog=dog_b).exists()
        and Like.objects.filter(from_dog=dog_b, to_dog=dog_a).exists()
    )


def prepare_messages(messages, my_dog):
    """
    Prepare messages with sender info for template rendering.

    Returns:
        List of dicts with message, is_sent, sender_avatar, sender_name.
    """
    result = []
    for msg in messages:
        result.append({
            "message": msg,
            "is_sent": msg.sender_dog_id == my_dog.id,
            "sender_avatar": (
                msg.sender_dog.profile_photo.url
                if msg.sender_dog.profile_photo
                else None
            ),
            "sender_name": msg.sender_dog.name,
        })
    return result


def get_thread_messages(dog_a, dog_b):
    """Return all messages between two dogs ordered by creation time."""
    return (
        Message.objects.filter(
            Q(sender_dog=dog_a, receiver_dog=dog_b)
            | Q(sender_dog=dog_b, receiver_dog=dog_a)
        )
        .select_related("sender_dog", "receiver_dog")
        .order_by("created_at")
    )


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
        return render(request, "messages/inbox.html", {"conversations": []})

    conversation_messages = (
        Message.objects.filter(
            Q(sender_dog=my_dog) | Q(receiver_dog=my_dog)
        )
        .select_related(
            "sender_dog",
            "sender_dog__owner",
            "receiver_dog",
            "receiver_dog__owner",
        )
    )

    conversations = {}
    for msg in conversation_messages:
        other_dog = (
            msg.receiver_dog
            if msg.sender_dog_id == my_dog.id
            else msg.sender_dog
        )
        if other_dog.id not in conversations:
            conversations[other_dog.id] = {
                "dog": other_dog,
                "owner": other_dog.owner,
                "last_message": msg,
            }

    conversations_list = sorted(
        conversations.values(),
        key=lambda x: x["last_message"].created_at,
        reverse=True,
    )

    first_receiver_dog = None
    first_messages = []
    form = None
    matched = False

    if dog_id:
        for conv in conversations_list:
            if conv["dog"].id == dog_id:
                first_receiver_dog = conv["dog"]
                break
        if not first_receiver_dog:
            first_receiver_dog = Dog.objects.filter(id=dog_id).first()
    elif conversations_list:
        first_receiver_dog = conversations_list[0]["dog"]

    if first_receiver_dog:
        matched = is_match(my_dog, first_receiver_dog)
        form = MessageForm()
        first_messages = prepare_messages(
            get_thread_messages(my_dog, first_receiver_dog),
            my_dog,
        )

    if request.method == "POST" and first_receiver_dog:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender_dog = my_dog
            message.receiver_dog = first_receiver_dog
            message.save()
            return redirect(
                "messages_inbox_with_dog",
                dog_id=first_receiver_dog.id,
            )

    return render(
        request,
        "messages/inbox.html",
        {
            "conversations": conversations_list,
            "first_receiver_dog": first_receiver_dog,
            "first_messages": first_messages,
            "form": form,
            "my_dog": my_dog,
            "is_match": matched,
        },
    )


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

    if not is_match(my_dog, receiver_dog):
        return redirect("matches_list")

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

    return render(
        request,
        "messages/thread.html",
        {
            "receiver_dog": receiver_dog,
            "my_dog": my_dog,
            "messages": prepare_messages(
                get_thread_messages(my_dog, receiver_dog),
                my_dog,
            ),
            "form": form,
            "is_match": True,
        },
    )


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

    if not is_match(my_dog, receiver_dog):
        return redirect("matches_list")

    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender_dog = my_dog
        message.receiver_dog = receiver_dog
        message.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "message": {
                    "content": message.content,
                    "time": message.created_at.strftime("%I:%M %p"),
                    "is_sent": True,
                    "avatar": (
                        my_dog.get_photo_url()
                        if my_dog.profile_photo
                        else None
                    ),
                },
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
    get_thread_messages(my_dog, receiver_dog).delete()

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

    messages_data = [
        {
            "content": msg.content,
            "time": msg.created_at.strftime("%H:%M"),
            "is_sent": msg.sender_dog_id == my_dog.id,
        }
        for msg in get_thread_messages(my_dog, receiver_dog)
    ]

    return JsonResponse({"messages": messages_data})
