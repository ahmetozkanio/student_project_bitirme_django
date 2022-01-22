from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^lessons/lesson/(?P<lesson_id>\d+)$', consumers.LessonConsumers.as_asgi()),
    #path('lessons/lesson/<lesson_id>', consumers.LessonConsumers.as_asgi()),

]