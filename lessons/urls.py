from django.urls import path
from . import views


urlpatterns = [
    path('',views.lesson_list,name="lessons"),
    path('lesson/<int:lesson_id>',views.lesson_detail,name="lesson_detail"),
    path("lesson-create/",views.lesson_create,name = 'lesson_create'),

    path('attendace_remove/<int:attendance_id>',views.attendance_remove,name="attendance_remove"),
    path('lesson_add/',views.lesson_add,name="lesson_add"),
    path('attendances/',views.attendance_list ,name="attendances"),
    path('attendance/<int:attendance_id>',views.attendance_detail,name="attendance_detail"),
    path("announcements/",views.announcement_list,name = 'announcements'),
    path("announcement/<int:announcement_id>",views.announcement_detail,name = 'announcement_detail'),
    path("announcement-add/",views.announcement_add,name = 'announcement_add'),
    path("announcement-update/<int:announcement_id>",views.announcement_update,name = 'announcement_update'),
    path("announcement-delete/<int:announcement_id>",views.announcement_delete,name = 'announcement_delete'),
    path("attendance//<int:attendance_id>/qr",views.qr_site,name = 'qr'),

    path('lesson/<int:lesson_id>/attendance/<int:attendance_id>',views.attendance_add,name="attendance_add"),

    # path("attendance/<int:attendance_id>/login",views.attendance_user_joined,name="attendance_user_joined"),
]