from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<uuid:pk>/', consumers.NotificationConsumer.as_asgi()),
]