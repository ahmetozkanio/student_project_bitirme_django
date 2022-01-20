import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import lessons.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            lessons.routing.websocket_urlpatterns
        
        )
    ),
})
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
            
#        websocket_urlpatterns
#         )
#     ),
# })

