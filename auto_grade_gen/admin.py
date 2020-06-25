from django.contrib import admin
from .models import AutoGenCourse


class AutoGenCourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_id', 'active', 'last_gen_time')

admin.site.register(AutoGenCourse, AutoGenCourseAdmin)
