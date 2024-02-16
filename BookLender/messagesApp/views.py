# Adapted from https://www.photondesigner.com/articles/instant-messenger?ref=rdjango-instant-messenger


# Import necessary Django and Python libraries for handling HTTP requests, asynchronous operations, and JSON serialization.
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import sync_to_async
from typing import AsyncGenerator
import asyncio
from django.shortcuts import render, redirect
from django.http import HttpRequest, StreamingHttpResponse, HttpResponse
from . import models  # Import local models module for database access
import json
from .models import ChatRoom, Message  # Import specific models used in this application

def lobby(request):
    """
    View function for the chat lobby. Users can select an existing chat room or create a new one.
    """
    if request.method == 'POST':
        # Handle form submission for creating/joining a chat room
        room_name = request.POST.get('room_name')
        username = request.POST.get('username')
        request.session['username'] = username  # Store the username in the session
        chat_room, created = ChatRoom.objects.get_or_create(name=room_name)  # Create or get existing room
        return redirect('chat', room_name=chat_room.name)  # Redirect to the chat room view
    else:
        # Display the lobby with a list of available chat rooms for GET requests
        rooms = ChatRoom.objects.all()
        return render(request, 'lobby.html', {'rooms': rooms})

def chat(request, room_name):
    """
    View function for displaying a chat room and its messages.
    """
    if not request.session.get('username'):
        return redirect('lobby')  # Redirect to lobby if no username is set in session
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)  # Get or create the specified chat room
    messages = Message.objects.filter(chat_room=chat_room).order_by('created_at')  # Retrieve messages for the room
    return render(request, 'chat.html', {'room': chat_room, 'messages': messages})

def create_message(request: HttpRequest) -> HttpResponse:
    """
    Endpoint for creating a new message in a chat room.
    """
    content = request.POST.get("content")
    username = request.session.get("username")
    if not username:
        return HttpResponse(status=403)  # Return 403 Forbidden if no username is found in session

    author, _ = models.Author.objects.get_or_create(name=username)  # Get or create the author based on username

    if content:
        models.Message.objects.create(author=author, content=content)  # Create a new message if content is provided
        return HttpResponse(status=201)  # Return 201 Created for successful message creation
    else:
        return HttpResponse(status=400)  # Return 400 Bad Request if no content is provided

async def stream_chat_messages(request: HttpRequest) -> StreamingHttpResponse:

    async def event_stream():
        """
        Asynchronous generator to stream chat messages to the client.
        """
        # Stream existing messages first, regardless of last_id
        messages = await get_existing_messages()
        for message in messages:
            message_json = json.dumps(message, cls=DjangoJSONEncoder)
            yield f"data: {message_json}\n\n"

        last_id = await get_last_message_id()  # Get the ID of the last message

        # Continuously check for and stream new messages
        while True:
            new_messages = await get_new_messages(last_id)
            for message in new_messages:
                message_json = json.dumps(message, cls=DjangoJSONEncoder)  # Serialize message to JSON
                yield f"data: {message_json}\n\n"  # Yield the message data to the client
                last_id = message['id']  # Update last_id to the latest message ID
            await asyncio.sleep(1)  # Sleep to prevent constant database polling

    @sync_to_async
    def get_existing_messages():
        """
        Fetch existing messages to stream initially.
        """
        return list(models.Message.objects.all().order_by('created_at').values(
            'id', 'author__name', 'content', 'created_at'
        ))

    @sync_to_async
    def get_new_messages(last_id):
        """
        Fetch new messages since the given last_id.
        """
        return list(models.Message.objects.filter(id__gt=last_id).order_by('created_at').values(
            'id', 'author__name', 'content', 'created_at'
        ))

    @sync_to_async
    def get_last_message_sync():
        """
        Synchronously fetch the last message.
        """
        return models.Message.objects.all().last()

    async def get_last_message_id():
        """
        Asynchronously get the ID of the last message.
        """
        last_message = await get_last_message_sync()
        return last_message.id if last_message else None

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
