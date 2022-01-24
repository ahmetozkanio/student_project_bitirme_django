from django.contrib import admin
from . models import Announcement, Attendance, Lesson, LessonFiles, Message, OnlineUsers
from import_export import resources
from django.contrib import admin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.hashers import make_password
# Register your models here.

admin.site.register(OnlineUsers)
admin.site.register(LessonFiles)

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




# Register your models here.
class UserResource(resources.ModelResource):

    def before_import_row(self,row,**kwargs):
        value = row['password']
        row['password'] = make_password(value)

    class Meta:
        model = User
        fields = ('username','password','first_name', 'last_name', 'email')
        
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)