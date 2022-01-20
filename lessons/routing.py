from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^lessons/lesson/(?P<pk>\d+)$', consumers.LessonConsumers.as_asgi()),
]