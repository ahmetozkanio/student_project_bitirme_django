from django.urls import path
from . import views


urlpatterns = [
    path('',views.event_list,name="events"),
    path("event-create/",views.event_create,name = 'event_create'),
    path("event-join/",views.event_join,name = 'event_join'),
    
    path('event/<int:event_id>',views.event_detail,name="event_detail"),
]