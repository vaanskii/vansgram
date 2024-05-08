import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from account.models import User

class NotificationConsumer(AsyncWebsocketConsumer):
    pass