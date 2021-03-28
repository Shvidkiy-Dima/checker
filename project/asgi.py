import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from monitor.routing import websocket_urlpatterns
from utils.middlewares import TokenAuthMiddlewareStack


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
                    # TODO: token must be in Query!
                    TokenAuthMiddlewareStack(
                        URLRouter(websocket_urlpatterns)
                        )
                    )
                }
    )