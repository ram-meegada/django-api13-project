from django.contrib import admin
from .models import Course
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'taken_by']
admin.site.register(Course, CourseAdmin)