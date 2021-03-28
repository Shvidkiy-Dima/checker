from django.urls import path
from monitor import consumers

websocket_urlpatterns = [
    path('ws/dashboard/', consumers.MessageConsumer.as_asgi()),
]