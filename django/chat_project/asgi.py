"""
ASGI config for chat_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_project.settings")
django_asgi_app = get_asgi_application()

import chat_app.routing

# Let the ProtocolTypeRouter figure out if this is a
# normal HTTP request that should have HTML sent back,
# or a WebSocket request that should be handled by the
# Django Channels stuff
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        # Use authentication for protected WebSocket
        # connections
        AuthMiddlewareStack(
            # Route the WebSocket connection based on the
            # URL path
            URLRouter(
                chat_app.routing.websocket_urlpatterns,
            )
        )
    ),
})
