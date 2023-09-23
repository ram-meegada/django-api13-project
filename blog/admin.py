from django.contrib import admin
# Register your models here.
from .models import Description, Course, Friend, User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('written_by', 'description')

class FriendAdmin(admin.ModelAdmin):
    # fields = ('user', 'friend')
    list_display = ('user','all_friends')
    def all_friends(self, obj):
        return ', '.join([i.username for i in obj.friend.all()])  


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'all_course_selectors')
    def all_course_selectors(self, obj):
        return ', '.join([i.username for i in obj.course_opters.all()])   

fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields':('email', 'age', 'full_name')})
UserAdmin.fieldsets = tuple(fields)

class UserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        # (
        #     'Address details',
        #     {
        #         'fields':(
        #                 'state',
        #                 'city',
        #                 'zipcode',
        #                 'Address_line1',
        #                 'Address_line2'
        #         )
        #     },
        # ),
        ('Additional fields', {'fields':('is_verified',)})
    )     
# class UserAdmin(UserAdmin):
#     fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'Additional Info',
#             {
#                 'fields':(
#                         'is_verified',
#                 )
#             }
#         )
#     )     
#     list_display = ('username', 'email', 'is_verified')

# class VerificationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'is_verified')        

admin.site.register(Description, DescriptionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(User, UserAdmin)
# admin.site.register(Verification, VerificationAdmin)