from django.contrib import admin
from . models import Announcement, Attendance, Lesson, Message

# Register your models here.

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id','name','avaliable','date')
    list_filter = ('avaliable',)
    search_fields = ('name',"description")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id','lesson','date','date2','date_now','avaliable')
    list_filter = ('avaliable',)
    search_fields = ('lesson',"date_now")

    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','lesson','user','date')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id','lesson','title','date','avaliable')
    list_filter = ('avaliable',)
    search_fields = ('lesson',"title",'date')
