import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import gamehive.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamehive.settings")

application = ProtocolTypeRouter( 
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
               gamehive.routing.websocket_urlpatterns
            )
        ),
    }
)