from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from connections.models import Connection
from dogs.models import Dog
from profiles.models import OwnerProfile

from .forms import MessageForm
from .models import Message


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
    sent_messages = Message.objects.filter(
        sender_dog=my_dog
    ).select_related('receiver_dog', 'receiver_dog__owner')

    # Group by receiver dog (get latest message per conversation)
    conversations = {}
    for msg in sent_messages:
        receiver_id = msg.receiver_dog.id
        if receiver_id not in conversations:
            conversations[receiver_id] = {
                'dog': msg.receiver_dog,
                'owner': msg.receiver_dog.owner,
                'last_message': msg
            }

    # Sort by latest message first
    conversations_list = sorted(
        conversations.values(),
        key=lambda x: x['last_message'].created_at,
        reverse=True
    )

    # Load first conversation for desktop split view
    first_receiver_dog = None
    first_messages = []
    form = None
    is_match = False

    if conversations_list:
        first_receiver_dog = conversations_list[0]['dog']

        # Check if it's a match
        is_match = Connection.objects.filter(
            from_dog=my_dog,
            to_dog=first_receiver_dog
        ).exists() and Connection.objects.filter(
            from_dog=first_receiver_dog,
            to_dog=my_dog
        ).exists()

        # Get messages for first conversation
        messages = Message.objects.filter(
            sender_dog=my_dog,
            receiver_dog=first_receiver_dog
        ).order_by('created_at')

        for msg in messages:
            sender_avatar = (
                msg.sender_dog.profile_photo.url
                if msg.sender_dog.profile_photo
                else None
            )
            first_messages.append({
                'message': msg,
                'is_sent': msg.sender_dog.id == my_dog.id,
                'sender_avatar': sender_avatar,
                'sender_name': msg.sender_dog.name,
            })

        form = MessageForm()

    # Handle message sending from inbox
    if request.method == "POST" and first_receiver_dog:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender_dog = my_dog
            message.receiver_dog = first_receiver_dog
            message.save()
            return redirect("messages_inbox")

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

    # Prepare messages with sender info for template
    messages_with_sender = []
    for msg in messages:
        sender_avatar = (
            msg.sender_dog.profile_photo.url
            if msg.sender_dog.profile_photo
            else None
        )
        messages_with_sender.append({
            'message': msg,
            'is_sent': msg.sender_dog.id == my_dog.id,
            'sender_avatar': sender_avatar,
            'sender_name': msg.sender_dog.name,
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
        
        # If AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': {
                    'content': message.content,
                    'time': message.timestamp.strftime('%I:%M %p'),
                    'is_sent': True
                }
            })

    return redirect("message_thread", dog_id=dog_id)


@login_required
@require_POST
def delete_conversation(request, dog_id):
    """Delete all messages in a conversation"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile or not hasattr(owner_profile, "dog"):
        return redirect("browse_dogs")

    my_dog = owner_profile.dog
    receiver_dog = get_object_or_404(Dog, id=dog_id)

    # Delete all messages between these two dogs
    Message.objects.filter(
        sender_dog=my_dog,
        receiver_dog=receiver_dog
    ).delete()

    return redirect("messages_inbox")


@login_required
def get_conversation_messages(request, dog_id):
    """API endpoint to fetch messages for a conversation"""
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    if not owner_profile or not hasattr(owner_profile, "dog"):
        return JsonResponse({'error': 'No dog profile'}, status=400)

    my_dog = owner_profile.dog
    receiver_dog = get_object_or_404(Dog, id=dog_id)

    # Get all messages in this conversation
    messages = Message.objects.filter(
        sender_dog=my_dog,
        receiver_dog=receiver_dog
    ).order_by('created_at')

    messages_data = []
    for msg in messages:
        messages_data.append({
            'content': msg.content,
            'time': msg.created_at.strftime('%H:%M'),
            'is_sent': msg.sender_dog.id == my_dog.id,
        })

    return JsonResponse({'messages': messages_data})
