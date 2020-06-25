import os.path
import glob
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from auto_grade_gen.models import AutoGenCourse
from lms.djangoapps.instructor.views.api import calculate_grades_csv, require_level
from lms.djangoapps.instructor_task.api import submit_calculate_grades_csv
from django.http import HttpRequest
from django.contrib.auth.models import User
from lms.djangoapps.instructor_task.models import DjangoStorageReportStore, ReportStore
from opaque_keys.edx.keys import CourseKey
import hashlib
from shutil import move
import time

from six import text_type


request = HttpRequest()
request.method = 'POST'
request.META['SERVER_NAME'] = 'localhost'
request.META['REMOTE_ADDR'] = 'localhost'
request.META['SERVER_PORT'] = 0
request.user = User.objects.get(username="isankadn")


class Command(BaseCommand):

    help = 'Generate grades for specific courses'

    def handle(self, *args, **kwargs):

        # print (self.__dict__.keys())
        # print (request.__dict__.keys())

        course_ids = AutoGenCourse.objects.filter(active=True)
        for x in course_ids:
            print (x.course_id)

            course_key = CourseKey.from_string(x.course_id)
            submit_calculate_grades_csv(request, course_key)

            print ('wait for finish to generate report.....')

            time.sleep(60)
            print ('starting renaming and move the FTP location.....')


            hashed_course_id = hashlib.sha1(text_type(x.course_id)).hexdigest()


            report_store = ReportStore.from_config('GRADES_DOWNLOAD')
            report_location = os.path.join(report_store.storage.base_location, hashed_course_id)
            rename_file = os.path.join(report_location, x.course_name + '.csv')
            ftp_locaiton = os.path.join('/sftp/shopwareit/upload', x.course_name + '.csv')
            list_of_files = glob.glob(report_location+ '/*')

            if list_of_files:
                latest_file = max(list_of_files, key=os.path.getctime)

                print (x.course_name)
                print('location:' + report_location)
                print ('rename_file:' + rename_file)
                move(latest_file, rename_file)
                move(rename_file, ftp_locaiton)


            #/tmp/edx-s3/grades/
            #path = report_store.path_to(x.course_id)
            #print (report_store.storage.location)
            #print (report_store.storage.base_location)


            #time = timezone.now().strftime('%X')
            #self.stdout.write("It's now %s" % time)

            
