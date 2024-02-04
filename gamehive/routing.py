from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from rock_paper_scissors import consumers

websocket_urlpatterns=[
                    re_path(
                        r"ws/multiplayer_rps/(?P<room_id>\w+)/$", consumers.RockPaperScissorsConsumer.as_asgi()
                    ),
                ]

application = ProtocolTypeRouter( 
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
               websocket_urlpatterns
            )
        ),
    }
)