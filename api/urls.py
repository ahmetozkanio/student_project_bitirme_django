from django.urls import path
from . import views

urlpatterns = [
     #User#
     path('users/',views.getUsers),
     #Event#
     path('events/',views.getEvents),


     path('lessons/',views.getLessons),
     path('lesson/create',views.createLesson),
     path('lesson/<int:id>/update',views.updateLesson),
     path('lesson/<int:id>/delete',views.deleteLesson),
     path('lesson/<int:id>',views.getLesson),
     #Attendance#
     path('attendances/',views.getAttendances),
     #Message#
     path('lesson/<int:lesson_id>/messages/',views.getMessage),
     path('messages/',views.getMessages),





]
