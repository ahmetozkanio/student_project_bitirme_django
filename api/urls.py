from django.urls import path
from . import views

urlpatterns = [
     #User#
     path('users/',views.getUsers),


     path('lessons/',views.getLessons),
     path('lesson/create',views.createLesson),
     path('lesson/<int:id>/update',views.updateLesson),
     path('lesson/<int:id>/delete',views.deleteLesson),
     path('lesson/<int:id>',views.getLesson),
     #Attendance#
     path('attendances/',views.getAttendances),
     #Message#
     path('message/<int:id>',views.getMessages),




]
