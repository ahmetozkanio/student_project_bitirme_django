from django.urls import path
from . import views

urlpatterns = [
     #User#
     path('users/',views.getUsers),

   
     #Event#
     path('events/',views.EventList.as_view()),


     path('lessons/',views.LessonList.as_view()),


     path('lesson/<int:id>',views.LessonDetail.as_view()),
     #Attendance#
     path('attendances/',views.AttendanceList.as_view()),
     #Message#
     path('lesson/<int:lesson_id>/messages/',views.MessageDetail.as_view()),
     path('messages/',views.MessageList.as_view()),






]
