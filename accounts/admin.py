# from import_export import resources
# from django.contrib import admin
# from django.contrib.auth.models import User
# from import_export.admin import ImportExportModelAdmin,ImportMixin
# from django.contrib.auth.hashers import make_password

# Register your models here.
# class UserResource(resources.ModelResource):

#     def before_import_row(self,row,**kwargs):
#         value = row['password']
#         row['password'] = make_password(value)

#     class Meta:
#         model = User
#         fields = ('username','password','first_name', 'last_name', 'email')
        
#     def get_instance(self, instance_loader, row):
#         try:
#             params = {}
#             for key in instance_loader.resource.get_import_id_fields():
#                 field = instance_loader.resource.fields[key]
#                 params[field.attribute] = field.clean(row)
#             return self.get_queryset().get(**params)
#         except Exception:
#             return None


# class UserAdmin(ImportExportModelAdmin):
#     resource_class = UserResource


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)






# class CustomBookAdmin(ImportMixin, admin.ModelAdmin):
#     resource_class = UserResource

#     def get_import_form(self):
#         return ImportForm

#     def get_confirm_import_form(self):
#         return ConfirmImportForm

#     def get_form_kwargs(self, form, *args, **kwargs):
#          # pass on `author` to the kwargs for the custom confirm form
#         # if isinstance(form, ImportForm):
#         #     if form.is_valid():
#         #         author = form.cleaned_data['author']
#         #         kwargs.update({'author': author.id})
#         return kwargs
# admin.site.register(User, CustomBookAdmin)