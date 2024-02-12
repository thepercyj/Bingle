# Adapted from https://www.photondesigner.com/articles/instant-messenger?ref=rdjango-instant-messenger


from datetime import datetime
from typing import AsyncGenerator
import asyncio
from django.shortcuts import render, redirect
from django.http import HttpRequest, StreamingHttpResponse, HttpResponse
from . import models
import json
from .models import ChatRoom, Message

def lobby(request):
    """
    Handles the lobby where users can choose or create a chat room.
    """
    if request.method == 'POST':
        # Get room name and username from the form
        room_name = request.POST.get('room_name')
        username = request.POST.get('username')
        # Save username in session
        request.session['username'] = username
        # Create or get the chat room
        chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
        # Redirect to the chat room
        return redirect('chat', room_name=chat_room.name)
    else:
        # Display available chat rooms
        rooms = ChatRoom.objects.all()
        return render(request, 'lobby.html', {'rooms': rooms})

def chat(request, room_name):
    """
    Handles the chat view where messages of a chat room are displayed.
    """
    # Redirect to lobby if username not set in session
    if not request.session.get('username'):
        return redirect('lobby')
    # Create or get the chat room
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    # Get messages for the chat room
    messages = Message.objects.filter(chat_room=chat_room).order_by('created_at')
    return render(request, 'chat.html', {'room': chat_room, 'messages': messages})

def create_message(request: HttpRequest) -> HttpResponse:
    """
    Creates a new message in a chat room.
    """
    content = request.POST.get("content")
    username = request.session.get("username")
    if not username:
        return HttpResponse(status=403)

    # Create or get the author
    author, _ = models.Author.objects.get_or_create(name=username)

    if content:
        # Create message if content is provided
        models.Message.objects.create(author=author, content=content)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)  # Return 400 (Bad Request) instead of 200 to indicate no content was provided.

async def stream_chat_messages(request: HttpRequest) -> StreamingHttpResponse:
    """
    Streams chat messages to the client as new messages are created.
    """

    async def event_stream():
        """
        Sends a continuous stream of data to the connected clients.
        """
        # Stream existing messages
        async for message in get_existing_messages():
            yield message

        # Get last message ID to check for new messages
        last_id = await get_last_message_id()

        # Continuously check for and stream new messages
        while True:
            new_messages = models.Message.objects.filter(id__gt=last_id).order_by('created_at').values(
                'id', 'author__name', 'content'
            )
            async for message in new_messages:
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message['id']
            await asyncio.sleep(0.1)  # Throttle checks to reduce database queries

    async def get_existing_messages() -> AsyncGenerator:
        """
        Generator for existing messages to be streamed initially.
        """
        messages = models.Message.objects.all().order_by('created_at').values(
            'id', 'author__name', 'content'
        )
        async for message in messages:
            yield f"data: {json.dumps(message)}\n\n"

    async def get_last_message_id() -> int:
        """
        Retrieves the ID of the last message sent.
        """
        last_message = await models.Message.objects.all().last()
        return last_message.id if last_message else 0

    # Return a streaming HTTP response with the event stream
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
