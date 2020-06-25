from django.db import models


class AutoGenCourse(models.Model):
    course_id = models.CharField(verbose_name="Course ID", max_length=100, unique=True)
    active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    course_name = models.CharField(verbose_name="Course Name", max_length=100, unique=True, null=True)
    last_gen_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['course_id']