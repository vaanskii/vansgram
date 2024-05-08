from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/notification/<uuid:pk>/', consumers.NotificationConsumer.as_asgi()),
]