from django.contrib import admin
from . models import Announcement, Attendance, Lesson, LessonFiles, Message, OnlineUsers
from import_export import resources
from django.contrib import admin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin,ImportMixin
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


# class UserAdmin(ImportExportModelAdmin):
#     resource_class = UserResource

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)








# class UserResource(resources.ModelResource):

#     class Meta:
#         model = User



from .forms import ImportForm,cConfirmImportForm
# import module
import openpyxl

from django.utils.encoding import force_str

class CustomBookAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = UserResource
    
    

    def get_import_form(self):
        return ImportForm

    def get_confirm_import_form(self):       
        return cConfirmImportForm

    # def process_import(request, *args, **kwargs):
    #     print(request)
    #     return kwargs

    def get_form_kwargs(self, form, *args, **kwargs):
        #  pass on `author` to the kwargs for the custom confirm form
        self.lessonUserAddList = []

        if isinstance(form, ImportForm):
            if form.is_valid():

                file = form.cleaned_data['import_file'] 
                # load excel with its path
                wrkbk = openpyxl.load_workbook(file)
                sh = wrkbk.active
                # iterate through excel and display data
                for row in sh.iter_rows(max_col=1):
                    for cell in row:
                        self.lessonUserAddList.append(cell.value)
                        print(cell.value, end=" ")

                self.lesson = form.cleaned_data['lesson']
                self.lessonUserAddList.remove('username')   

                kwargs.update({'self.lesson': self.lesson.id})
            
        elif isinstance(form, cConfirmImportForm):
            if form.is_valid():
                print("confirm form ")
                lesson = form.cleaned_data['lesson']
                lessonObj = Lesson.objects.get(name=lesson)
                print(lessonObj)
                for userList in self.lessonUserAddList:
                    user = User.objects.get(username= userList)
                    lessonObj.students.add(user)
                kwargs.update({'id_lesson': lesson})
        return kwargs

    
    def process_import(self, request, *args, **kwargs):
        """
        Perform the actual import action (after the user has confirmed the import)
         """

        form_type = self.get_confirm_import_form()
        confirm_form = form_type(request.POST)
        if confirm_form.is_valid():


            print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
            

        
          
            print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
            print(confirm_form)
            lesson = confirm_form.cleaned_data['lessonn']
            lessonObj = Lesson.objects.get(name=lesson)
            print(lessonObj)

            import_formats = self.get_import_formats()

            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            tmp_storage = self.get_tmp_storage_class()(name=confirm_form.cleaned_data['import_file_name'])
            data = tmp_storage.read(input_format.get_read_mode())
            if not input_format.is_binary() and self.from_encoding:
                data = force_str(data, self.from_encoding)
            dataset = input_format.create_dataset(data)
            result = self.process_dataset(dataset, confirm_form, request, *args, **kwargs)
            tmp_storage.remove()


            for userList in self.lessonUserAddList:
                user =  User.objects.get(username= userList)
                lessonObj.students.add(user)



            return self.process_result(result, request)
          


admin.site.unregister(User)
admin.site.register(User, CustomBookAdmin)



            


  

