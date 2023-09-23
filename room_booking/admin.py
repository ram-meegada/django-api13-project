from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'Additional Info',
#             {
#                 'fields':(
#                         'age',
#                 )
#             }
#         )
#     )
fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal info',{'fields':('first_name','last_name','email','age')})
UserAdmin.fieldsets = tuple(fields)
admin.site.register(CustomUser, UserAdmin)
# admin.site.register(CustomUser, CustomUserAdmin)