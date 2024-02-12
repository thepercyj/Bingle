# Adapted from https://www.photondesigner.com/articles/instant-messenger?ref=rdjango-instant-messenger


from datetime import datetime

from typing import AsyncGenerator
import asyncio
from django.shortcuts import render, redirect
from django.http import HttpRequest, StreamingHttpResponse, HttpResponse
from . import models
import json
from django.shortcuts import render, redirect
from .models import ChatRoom, Message


def lobby(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        username = request.POST.get('username')  # Get username from the form
        request.session['username'] = username  # Save username in session
        chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
        return redirect('chat', room_name=chat_room.name)  # Adjust redirection if necessary
    else:
        rooms = ChatRoom.objects.all()
        return render(request, 'lobby.html', {'rooms': rooms})



def chat(request, room_name):
    if not request.session.get('username'):
        return redirect('lobby')
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    messages = Message.objects.filter(chat_room=chat_room).order_by('created_at')
    return render(request, 'chat.html', {'room': chat_room, 'messages': messages})


def create_message(request: HttpRequest) -> HttpResponse:
    content = request.POST.get("content")
    username = request.session.get("username")
    if not username:
        return HttpResponse(status=403)

    print(username)
    author, _ = models.Author.objects.get_or_create(name=username)

    if content:
        models.Message.objects.create(author=author, content=content)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=200)


async def stream_chat_messages(request: HttpRequest) -> StreamingHttpResponse:
    """
    Streams chat messages to the client as we create messages.
    """

    async def event_stream():
        """
        We use this function to send a continuous stream of data
        to the connected clients.
        """
        async for message in get_existing_messages():
            yield message

        last_id = await get_last_message_id()

        # Continuously check for new messages
        while True:
            new_messages = models.Message.objects.filter(id__gt=last_id).order_by('created_at').values(
                'id', 'author__name', 'content'
            )
            async for message in new_messages:
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message['id']
            await asyncio.sleep(0.1)  # Adjust sleep time as needed to reduce db queries.

    async def get_existing_messages() -> AsyncGenerator:
        messages = models.Message.objects.all().order_by('created_at').values(
            'id', 'author__name', 'content'
        )
        async for message in messages:
            yield f"data: {json.dumps(message)}\n\n"

    async def get_last_message_id() -> int:
        last_message = await models.Message.objects.all().alast()
        return last_message.id if last_message else 0

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
