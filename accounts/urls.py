
from django.urls import path
from accounts import views



urlpatterns = [
    path("register/",views.register,name = 'register'),
    path("login/",views.login,name = 'login'),
    path("logout/",views.logout,name = 'logout'),
    path("dashboard/",views.user_dashboard,name = 'dashboard'),
    path("lesson/<int:lesson_id>/attendance/<int:attendance_id>/login",views.attendance_joined,name="attendance_user_joined"),
]
