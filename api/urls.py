from django.urls import path
from . import views
from rest_framework.authtoken import views as token
urlpatterns = [
     #User#
     path('users/',views.getUsers),
     path('api-token-auth/', views.CustomAuthToken.as_view()),
     path('register/', views.RegisterView.as_view()),
     
     #Event#
     path('events/',views.EventList.as_view()),


     path('lessons/',views.getLessons),
     path('lesson/add',views.postLesson),



     path('lesson/<int:id>',views.LessonDetail.as_view()),
     #Attendance#
     path('attendances/',views.AttendanceList.as_view()),
     #Message#
     path('lesson/<int:lesson_id>/messages/',views.MessageDetail.as_view()),
     path('messages/',views.postMessage),
     #announcement#
     path('announcements/',views.AnnouncementList.as_view()),







]
