from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from profiles.models import OwnerProfile
from dogs.models import Dog
from connections.models import Connection
from .models import Message
from .forms import MessageForm


@login_required
def messages_inbox(request):
    """Display all messages sent by user's dog"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile or not hasattr(owner_profile, "dog"):
        return render(
            request,
            "messages/inbox.html",
            {"conversations": []}
        )

    my_dog = owner_profile.dog

    # Get all unique receiver dogs with their last message
    sent_messages = Message.objects.filter(sender_dog=my_dog).select_related(
        'receiver_dog', 'receiver_dog__owner'
    )

    # Group by receiver dog (get latest message per conversation)
    conversations = {}
    for msg in sent_messages:
        receiver_id = msg.receiver_dog.id
        if receiver_id not in conversations:
            conversations[receiver_id] = {
                'dog': msg.receiver_dog,
                'owner': msg.receiver_dog.owner,
                'last_message': msg,
                'message_count': 0
            }
        conversations[receiver_id]['message_count'] += 1

    # Sort by latest message first
    conversations_list = sorted(
        conversations.values(),
        key=lambda x: x['last_message'].created_at,
        reverse=True
    )

    return render(
        request,
        "messages/inbox.html",
        {"conversations": conversations_list}
    )


@login_required
def message_thread(request, dog_id):
    """Display conversation with a specific dog"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile or not hasattr(owner_profile, "dog"):
        return redirect("browse_dogs")

    my_dog = owner_profile.dog
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
        sender_dog=my_dog,
        receiver_dog=receiver_dog
    ).order_by('created_at')

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
        "messages": messages,
        "form": form,
        "is_match": is_match
    }

    return render(request, "messages/thread.html", context)


@login_required
@require_POST
def send_message(request, dog_id):
    """Quick send message from matches page"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile or not hasattr(owner_profile, "dog"):
        return redirect("browse_dogs")

    my_dog = owner_profile.dog
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

    return redirect("message_thread", dog_id=dog_id)
