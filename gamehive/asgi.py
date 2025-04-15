import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamehive.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

asgi_application = get_asgi_application()

import gamehive.routing

application = ProtocolTypeRouter( 
    {
        "http": asgi_application,
        "websocket": AuthMiddlewareStack(
            URLRouter(
               gamehive.routing.websocket_urlpatterns
            )
        ),
    }
)