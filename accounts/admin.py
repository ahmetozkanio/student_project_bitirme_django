from import_export import resources
from django.contrib import admin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('username','password','first_name', 'last_name', 'email')


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)